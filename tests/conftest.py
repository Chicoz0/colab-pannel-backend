import pytest

from app.database import Base, SessionLocal, engine


@pytest.fixture
def db_session():
    """Create the tables from the ORM models, hand the test a session,
    then drop everything afterwards so tests never pollute each other."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
