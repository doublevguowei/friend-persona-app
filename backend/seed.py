from database import Base, SessionLocal, engine
from models import DailyQuestion, Question, User, Vote  # noqa: F401
from seed_data import QUESTIONS, USERS, seed_database


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        print(f"Seed complete: {len(USERS)} users, {len(QUESTIONS)} questions.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
