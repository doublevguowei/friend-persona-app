import os
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import DailyQuestion, Question, User, Vote
from schemas import VoteCreate
from seed_data import TRAIT_KEYS, TRAIT_MAP, TRAITS, seed_database


APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Asia/Shanghai")

app = FastAPI(title="群友人格档案馆 API", version="0.1.0")

cors_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


def today() -> date:
    return datetime.now(ZoneInfo(APP_TIMEZONE)).date()


def user_to_dict(user: User) -> dict:
    scores = {key: getattr(user, key) for key in TRAIT_KEYS}
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "scores": scores,
        **scores,
    }


def question_to_dict(question: Question) -> dict:
    return {
        "id": question.id,
        "text": question.text,
        "category": question.category,
        "trait_key": question.trait_key,
        "trait_name": TRAIT_MAP[question.trait_key]["name"],
    }


def get_daily_questions(db: Session, day: date) -> list[Question]:
    existing = (
        db.query(DailyQuestion)
        .filter(DailyQuestion.day == day)
        .order_by(DailyQuestion.position.asc())
        .all()
    )
    if len(existing) >= 4:
        return [item.question for item in existing[:4]]

    selected_ids = {item.question_id for item in existing}
    needed = 4 - len(existing)
    questions = db.query(Question).order_by(Question.id.asc()).all()

    recent_start = day - timedelta(days=7)
    recent_ids = {
        row[0]
        for row in db.query(DailyQuestion.question_id)
        .filter(DailyQuestion.day >= recent_start, DailyQuestion.day < day)
        .all()
    }

    preferred = [question for question in questions if question.id not in recent_ids and question.id not in selected_ids]
    fallback = [question for question in questions if question.id not in selected_ids and question.id not in {q.id for q in preferred}]

    rng = random.Random(day.isoformat())
    rng.shuffle(preferred)
    rng.shuffle(fallback)
    additions = (preferred + fallback)[:needed]

    start_position = len(existing) + 1
    for index, question in enumerate(additions, start=start_position):
        db.add(DailyQuestion(day=day, question_id=question.id, position=index))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    refreshed = (
        db.query(DailyQuestion)
        .filter(DailyQuestion.day == day)
        .order_by(DailyQuestion.position.asc())
        .all()
    )
    return [item.question for item in refreshed[:4]]


def get_vote_counts(db: Session, question_id: int, vote_day: date) -> dict[int, int]:
    rows = (
        db.query(Vote.target_id, func.count(Vote.id))
        .filter(Vote.question_id == question_id, Vote.vote_date == vote_day)
        .group_by(Vote.target_id)
        .all()
    )
    return {target_id: count for target_id, count in rows}


def make_question_label(text: str) -> str:
    label = text.strip().rstrip("？?")
    if label.startswith("今天谁"):
        label = label.replace("今天谁", "", 1)
    return label.strip() or text.strip()


def make_commentary(name: str, question: Question, count: int) -> str:
    templates = [
        "{name} 今日 {trait_name} 指数异常升高，建议群友谨慎互动。",
        "系统检测到 {name} 在「{question}」中表现突出，属于稳定发挥。",
        "恭喜 {name} 获得今日称号：{question_label}。",
    ]
    template = templates[question.id % len(templates)]
    return template.format(
        name=name,
        trait_name=TRAIT_MAP[question.trait_key]["name"],
        question=question.text,
        question_label=make_question_label(question.text),
        count=count,
    )


def build_result_item(db: Session, question: Question, vote_day: date) -> dict:
    users = db.query(User).order_by(User.id.asc()).all()
    counts = get_vote_counts(db, question.id, vote_day)
    top_count = max(counts.values(), default=0)
    champion_ids = [user_id for user_id, count in counts.items() if count == top_count and top_count > 0]
    champions = [user_to_dict(user) for user in users if user.id in champion_ids]

    if champions:
        names = "、".join(champion["nickname"] for champion in champions)
        commentary = make_commentary(names, question, top_count)
    else:
        commentary = "这题暂时无人登顶，群友们还在观望。"

    return {
        "question": question_to_dict(question),
        "stats": [
            {
                "user": user_to_dict(user),
                "votes": counts.get(user.id, 0),
            }
            for user in users
        ],
        "champions": champions,
        "top_count": top_count,
        "commentary": commentary,
    }


def recent_titles_for_user(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    start_day = today() - timedelta(days=30)
    daily_items = (
        db.query(DailyQuestion)
        .filter(DailyQuestion.day >= start_day)
        .order_by(desc(DailyQuestion.day), DailyQuestion.position.asc())
        .all()
    )
    titles: list[dict] = []
    for item in daily_items:
        counts = get_vote_counts(db, item.question_id, item.day)
        top_count = max(counts.values(), default=0)
        if top_count <= 0 or counts.get(user_id, 0) != top_count:
            continue
        titles.append(
            {
                "date": item.day.isoformat(),
                "question": item.question.text,
                "title": make_question_label(item.question.text),
                "votes": top_count,
            }
        )
        if len(titles) >= limit:
            break
    return titles


def get_historical_trait_scores(db: Session, trait_key: str) -> dict[int, int]:
    rows = (
        db.query(Vote.target_id, func.count(Vote.id))
        .join(Question, Vote.question_id == Question.id)
        .filter(Question.trait_key == trait_key)
        .group_by(Vote.target_id)
        .all()
    )
    return {target_id: count for target_id, count in rows}


@app.get("/health")
def health() -> dict:
    return {"ok": True, "date": today().isoformat()}


@app.get("/users")
def list_users(db: Session = Depends(get_db)) -> list[dict]:
    users = db.query(User).order_by(User.id.asc()).all()
    return [user_to_dict(user) for user in users]


@app.get("/daily-questions")
def list_daily_questions(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    if user_id is not None and db.get(User, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有这个群友身份")

    vote_day = today()
    questions = get_daily_questions(db, vote_day)
    user_votes = {}
    if user_id is not None:
        votes = (
            db.query(Vote)
            .filter(Vote.voter_id == user_id, Vote.vote_date == vote_day)
            .all()
        )
        user_votes = {vote.question_id: vote for vote in votes}

    return {
        "date": vote_day.isoformat(),
        "questions": [
            {
                **question_to_dict(question),
                "has_voted": question.id in user_votes,
                "voted_target_id": user_votes[question.id].target_id if question.id in user_votes else None,
            }
            for question in questions
        ],
    }


@app.post("/vote")
def create_vote(payload: VoteCreate, db: Session = Depends(get_db)) -> dict:
    vote_day = today()
    voter = db.get(User, payload.voter_id)
    target = db.get(User, payload.target_id)
    question = db.get(Question, payload.question_id)

    if voter is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="投票人身份不存在")
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="被投票的群友不存在")
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="这道题不存在")
    if payload.voter_id == payload.target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能投自己，别太自恋")

    get_daily_questions(db, vote_day)
    is_today_question = (
        db.query(DailyQuestion)
        .filter(DailyQuestion.day == vote_day, DailyQuestion.question_id == payload.question_id)
        .first()
        is not None
    )
    if not is_today_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="这不是今天的问题，先别穿越")

    already_voted = (
        db.query(Vote)
        .filter(
            Vote.voter_id == payload.voter_id,
            Vote.question_id == payload.question_id,
            Vote.vote_date == vote_day,
        )
        .first()
    )
    if already_voted is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="你今天这题已经投过啦，明天再来整活")

    vote = Vote(
        voter_id=payload.voter_id,
        target_id=payload.target_id,
        question_id=payload.question_id,
        vote_date=vote_day,
    )
    setattr(target, question.trait_key, getattr(target, question.trait_key) + 1)
    db.add(vote)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="你今天这题已经投过啦，明天再来整活")

    db.refresh(target)
    return {
        "message": "投票成功，今日人格档案已更新",
        "date": vote_day.isoformat(),
        "target": user_to_dict(target),
        "trait_key": question.trait_key,
        "trait_name": TRAIT_MAP[question.trait_key]["name"],
    }


@app.get("/results/today")
def today_results(db: Session = Depends(get_db)) -> dict:
    vote_day = today()
    questions = get_daily_questions(db, vote_day)
    return {
        "date": vote_day.isoformat(),
        "results": [build_result_item(db, question, vote_day) for question in questions],
    }


@app.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)) -> dict:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有这个群友档案")

    vote_day = today()
    today_received = (
        db.query(func.count(Vote.id))
        .filter(Vote.target_id == user_id, Vote.vote_date == vote_day)
        .scalar()
    )
    total_received = db.query(func.count(Vote.id)).filter(Vote.target_id == user_id).scalar()

    return {
        "user": user_to_dict(user),
        "today_received_votes": today_received,
        "total_received_votes": total_received,
        "recent_titles": recent_titles_for_user(db, user_id),
    }


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)) -> dict:
    boards = []
    users = db.query(User).order_by(User.id.asc()).all()
    for trait in TRAITS:
        scores = get_historical_trait_scores(db, trait["key"])
        ranked_users = sorted(users, key=lambda user: (-scores.get(user.id, 0), user.id))
        entries = []
        last_score = None
        rank = 0
        for index, user in enumerate(ranked_users, start=1):
            score = scores.get(user.id, 0)
            if score != last_score:
                rank = index
                last_score = score
            entries.append(
                {
                    "rank": rank,
                    "user": user_to_dict(user),
                    "score": score,
                }
            )
        boards.append(
            {
                "trait_key": trait["key"],
                "trait_name": trait["name"],
                "board_name": trait["board"],
                "scope": "all_history",
                "entries": entries,
            }
        )

    return {"date": today().isoformat(), "scope": "all_history", "leaderboards": boards}


if os.getenv("SERVE_FRONTEND", "false").lower() == "true":
    frontend_dist = Path(os.getenv("FRONTEND_DIST", "../frontend/dist")).resolve()
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str) -> FileResponse:
        index_file = frontend_dist / "index.html"
        requested_file = (frontend_dist / full_path).resolve()
        if full_path and requested_file.is_file() and frontend_dist in requested_file.parents:
            return FileResponse(requested_file)
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frontend build not found")
