from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    avatar: Mapped[str] = mapped_column(String(16), nullable=False)

    abstract_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stable_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tough_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leader_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    social_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    funny_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    emo_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wisdom_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lucky_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    caring_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    trait_key: Mapped[str] = mapped_column(String(32), nullable=False)


class DailyQuestion(Base):
    __tablename__ = "daily_questions"
    __table_args__ = (
        UniqueConstraint("day", "question_id", name="uq_daily_question"),
        UniqueConstraint("day", "position", name="uq_daily_position"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    day: Mapped[Date] = mapped_column(Date, index=True, nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped[Question] = relationship("Question")


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint("voter_id", "question_id", "vote_date", name="uq_vote_once_per_day"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    voter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)
    vote_date: Mapped[Date] = mapped_column(Date, index=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    voter: Mapped[User] = relationship("User", foreign_keys=[voter_id])
    target: Mapped[User] = relationship("User", foreign_keys=[target_id])
    question: Mapped[Question] = relationship("Question")
