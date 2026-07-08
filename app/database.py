from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.settings import settings


""" Create a new engine for the given database URL.
Now both testing and normal engines will have the same configuration
but they will be separate instances."""
def make_engine(database_url: str):
    return create_engine(database_url, pool_pre_ping=True)

# Create the engine for the normal database (none-test).
engine = make_engine(settings.database_url)

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
