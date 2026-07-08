from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.settings import settings

# Entry point to the database. This is the engine that will be used to connect to the database.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Not a session, but a factory for sessions ^^
SessionLocal = sessionmaker(bind=engine, autoflush=False)


"""
This is the base class for all models.
It carrys hidden metadata  of every table in the database
(because they are all instances of this class).
"""
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
