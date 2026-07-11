from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def make_engine(database_url: str):
    """Create a new engine for the given URL. Test and app engines share the
    same configuration but stay separate instances."""
    return create_engine(database_url, pool_pre_ping=True)


# Engine for the normal (non-test) database.
engine = make_engine(settings.database_url)


class Base(DeclarativeBase):
    """Base class for all models. Carries the metadata of every table."""

    pass
