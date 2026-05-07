from sqlalchemy.orm import Session

from models import Question, User


TRAITS = [
    {"key": "abstract_score", "name": "抽象值", "board": "抽象榜", "category": "抽象"},
    {"key": "stable_score", "name": "稳定值", "board": "稳定榜", "category": "稳定"},
    {"key": "tough_score", "name": "嘴硬值", "board": "嘴硬榜", "category": "嘴硬"},
    {"key": "leader_score", "name": "领导力", "board": "领导力榜", "category": "领导"},
    {"key": "social_score", "name": "社交值", "board": "社交榜", "category": "社交"},
    {"key": "funny_score", "name": "节目效果值", "board": "节目效果榜", "category": "节目效果"},
    {"key": "emo_score", "name": "emo值", "board": "emo榜", "category": "emo"},
    {"key": "wisdom_score", "name": "军师值", "board": "军师榜", "category": "军师"},
    {"key": "lucky_score", "name": "运气值", "board": "运气榜", "category": "运气"},
    {"key": "caring_score", "name": "情绪价值", "board": "情绪价值榜", "category": "情绪价值"},
]

TRAIT_MAP = {trait["key"]: trait for trait in TRAITS}
TRAIT_KEYS = [trait["key"] for trait in TRAITS]

USERS = [
    {"id": 1, "nickname": "龟哥", "avatar": "龟"},
    {"id": 2, "nickname": "丁丁", "avatar": "丁"},
    {"id": 3, "nickname": "李哥", "avatar": "李"},
    {"id": 4, "nickname": "二虎", "avatar": "虎"},
    {"id": 5, "nickname": "治泽", "avatar": "泽"},
    {"id": 6, "nickname": "柯柯", "avatar": "柯"},
]

QUESTIONS = [
    {"id": 1, "text": "今天谁最抽象？", "category": "抽象", "trait_key": "abstract_score"},
    {"id": 2, "text": "今天谁的发言最像随机生成的？", "category": "抽象", "trait_key": "abstract_score"},
    {"id": 3, "text": "今天谁最像一个没有说明书的人类？", "category": "抽象", "trait_key": "abstract_score"},
    {"id": 4, "text": "今天谁最像 NPC？", "category": "抽象", "trait_key": "abstract_score"},
    {"id": 5, "text": "今天谁今天的精神状态最难预测？", "category": "抽象", "trait_key": "abstract_score"},
    {"id": 6, "text": "今天谁最稳？", "category": "稳定", "trait_key": "stable_score"},
    {"id": 7, "text": "今天谁最像群里的定海神针？", "category": "稳定", "trait_key": "stable_score"},
    {"id": 8, "text": "今天谁最能扛事？", "category": "稳定", "trait_key": "stable_score"},
    {"id": 9, "text": "今天谁最适合在混乱时出来控场？", "category": "稳定", "trait_key": "stable_score"},
    {"id": 10, "text": "今天谁最像“问题不大”的人？", "category": "稳定", "trait_key": "stable_score"},
    {"id": 11, "text": "今天谁最嘴硬？", "category": "嘴硬", "trait_key": "tough_score"},
    {"id": 12, "text": "今天谁最像“我没事，你别管我”？", "category": "嘴硬", "trait_key": "tough_score"},
    {"id": 13, "text": "今天谁最可能嘴上说不在乎，心里已经记住了？", "category": "嘴硬", "trait_key": "tough_score"},
    {"id": 14, "text": "今天谁最像死鸭子嘴硬型选手？", "category": "嘴硬", "trait_key": "tough_score"},
    {"id": 15, "text": "今天谁最可能明明破防了还说自己很冷静？", "category": "嘴硬", "trait_key": "tough_score"},
    {"id": 16, "text": "今天谁最像老板？", "category": "领导", "trait_key": "leader_score"},
    {"id": 17, "text": "今天谁最适合当队长？", "category": "领导", "trait_key": "leader_score"},
    {"id": 18, "text": "今天谁最会安排事情？", "category": "领导", "trait_key": "leader_score"},
    {"id": 19, "text": "今天谁最像开会时负责总结的人？", "category": "领导", "trait_key": "leader_score"},
    {"id": 20, "text": "今天谁最有领导气质？", "category": "领导", "trait_key": "leader_score"},
    {"id": 21, "text": "今天谁最适合组织聚会？", "category": "社交", "trait_key": "social_score"},
    {"id": 22, "text": "今天谁最会活跃气氛？", "category": "社交", "trait_key": "social_score"},
    {"id": 23, "text": "今天谁最像社交局的核心人物？", "category": "社交", "trait_key": "social_score"},
    {"id": 24, "text": "今天谁最适合破冰？", "category": "社交", "trait_key": "social_score"},
    {"id": 25, "text": "今天谁最会接话？", "category": "社交", "trait_key": "social_score"},
    {"id": 26, "text": "今天谁最有节目效果？", "category": "节目效果", "trait_key": "funny_score"},
    {"id": 27, "text": "今天谁最像天生喜剧人？", "category": "节目效果", "trait_key": "funny_score"},
    {"id": 28, "text": "今天谁一开口就容易让群里热闹起来？", "category": "节目效果", "trait_key": "funny_score"},
    {"id": 29, "text": "今天谁最适合当群聊气氛组？", "category": "节目效果", "trait_key": "funny_score"},
    {"id": 30, "text": "今天谁今天最像短视频评论区？", "category": "节目效果", "trait_key": "funny_score"},
    {"id": 31, "text": "今天谁最容易 emo？", "category": "emo", "trait_key": "emo_score"},
    {"id": 32, "text": "今天谁最可能深夜突然思考人生？", "category": "emo", "trait_key": "emo_score"},
    {"id": 33, "text": "今天谁最像“没事但明显有事”？", "category": "emo", "trait_key": "emo_score"},
    {"id": 34, "text": "今天谁今天最需要被安慰？", "category": "emo", "trait_key": "emo_score"},
    {"id": 35, "text": "今天谁最可能突然打开伤感歌单？", "category": "emo", "trait_key": "emo_score"},
    {"id": 36, "text": "今天谁最适合当军师？", "category": "军师", "trait_key": "wisdom_score"},
    {"id": 37, "text": "今天谁最会分析局势？", "category": "军师", "trait_key": "wisdom_score"},
    {"id": 38, "text": "今天谁最适合给别人出主意？", "category": "军师", "trait_key": "wisdom_score"},
    {"id": 39, "text": "今天谁最像群里的战略顾问？", "category": "军师", "trait_key": "wisdom_score"},
    {"id": 40, "text": "今天谁最懂人情世故？", "category": "军师", "trait_key": "wisdom_score"},
    {"id": 41, "text": "今天谁最可能突然发财？", "category": "运气", "trait_key": "lucky_score"},
    {"id": 42, "text": "今天谁今天看起来运气最好？", "category": "运气", "trait_key": "lucky_score"},
    {"id": 43, "text": "今天谁最可能捡到便宜？", "category": "运气", "trait_key": "lucky_score"},
    {"id": 44, "text": "今天谁最像被命运偷偷照顾的人？", "category": "运气", "trait_key": "lucky_score"},
    {"id": 45, "text": "今天谁最可能抽奖中奖？", "category": "运气", "trait_key": "lucky_score"},
    {"id": 46, "text": "今天谁最会安慰人？", "category": "情绪价值", "trait_key": "caring_score"},
    {"id": 47, "text": "今天谁最能提供情绪价值？", "category": "情绪价值", "trait_key": "caring_score"},
    {"id": 48, "text": "今天谁最适合当树洞？", "category": "情绪价值", "trait_key": "caring_score"},
    {"id": 49, "text": "今天谁最会让别人安心？", "category": "情绪价值", "trait_key": "caring_score"},
    {"id": 50, "text": "今天谁最像温柔但嘴欠的朋友？", "category": "情绪价值", "trait_key": "caring_score"},
]


def seed_database(db: Session) -> None:
    for payload in USERS:
        user = db.get(User, payload["id"])
        if user is None:
            db.add(User(**payload))
        else:
            user.nickname = payload["nickname"]
            user.avatar = payload["avatar"]

    for payload in QUESTIONS:
        question = db.get(Question, payload["id"])
        if question is None:
            db.add(Question(**payload))
        else:
            question.text = payload["text"]
            question.category = payload["category"]
            question.trait_key = payload["trait_key"]

    db.commit()
