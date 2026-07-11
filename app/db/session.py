from sqlalchemy.orm import sessionmaker

from app.db.base import engine

# Not a session, but a factory for sessions.
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
