import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401  -> registers the models on Base.metadata
from app.database import Base, make_engine
from app.settings import settings

test_engine = make_engine(settings.test_database_url)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


@pytest.fixture
def db_session():
    """Create the tables in the TEST database, hand the test a session,
    then drop everything afterwards. Bound to colab_test, never colab."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)
