from sqlalchemy import select

from app.models import User


def test_user_persists_and_reads_back(db_session):
    db_session.add(
        User(
            username="johndoe",
            email="johndoe@example.com",
            full_name="John Doe",
            hashed_password="not-a-real-hash",
        )
    )
    db_session.commit()

    fetched = db_session.execute(
        select(User).where(User.username == "johndoe")
    ).scalar_one()

    assert fetched.id is not None
    assert fetched.username == "johndoe"
    assert fetched.email == "johndoe@example.com"
    assert fetched.full_name == "John Doe"
    assert fetched.disabled is False


def test_user_lives_in_the_app_schema():
    assert User.__tablename__ == "users"
    assert User.__table__.schema == "app"
