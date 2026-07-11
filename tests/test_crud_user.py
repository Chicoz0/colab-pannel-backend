from app.crud.user import get_user
from app.models import User
from app.schemas.user import UserInDB


def test_get_user_returns_userindb_when_present(db_session):
    db_session.add(
        User(
            username="johndoe",
            email="johndoe@example.com",
            full_name="John Doe",
            hashed_password="hashed-secret",
        )
    )
    db_session.commit()

    result = get_user(db_session, "johndoe")

    assert isinstance(result, UserInDB)
    assert result.username == "johndoe"
    assert result.hashed_password == "hashed-secret"
    assert result.disabled is False


def test_get_user_returns_none_when_absent(db_session):
    assert get_user(db_session, "ghost") is None
