from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext

from app.database import Base, make_engine
from app.settings import ROOT, settings
import app.models  # noqa: F401  -> registers the models on Base.metadata


def test_migrations_match_models():
    """The schema built by the migrations must equal the schema the models
    describe. Change a model without a matching migration -> this goes red."""
    alembic_cfg = Config(str(ROOT / "alembic.ini"))
    engine = make_engine(settings.test_database_url)

    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            alembic_cfg.attributes["connection"] = connection
            command.upgrade(alembic_cfg, "head")

            migration_context = MigrationContext.configure(
                connection, opts={"include_schemas": True}
            )
            diff = compare_metadata(migration_context, Base.metadata)
        finally:
            transaction.rollback()

    assert diff == [], f"Models and migrations diverged: {diff}"
