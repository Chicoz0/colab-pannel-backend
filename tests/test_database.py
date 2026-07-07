from sqlalchemy import text

from app.database import get_db


def _one_session():
    """gen = generator and db = session"""
    gen = get_db()
    db = next(gen)
    return gen, db


def test_get_db_yields_a_working_session():
    gen, db = _one_session()
    try:
        assert db.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        gen.close()


def test_config_points_at_the_colab_database_as_the_app_role():
    gen, db = _one_session()
    try:
        row = db.execute(
            text("SELECT current_database() AS db, current_user AS usr")
        ).one()
        assert row.db == "colab"
        assert row.usr == "colab_app"
    finally:
        gen.close()
