from app.core.security import get_password_hash
from app.models import User
from app.schemas.user import UserInDB
from app.services.auth import authenticate_user


def _seed(db):
    db.add(User(username="johndoe", hashed_password=get_password_hash("secret")))
    db.commit()


def test_authenticate_user_accepts_correct_password(db_session):
    _seed(db_session)

    user = authenticate_user(db_session, "johndoe", "secret")

    assert isinstance(user, UserInDB)
    assert user.username == "johndoe"


def test_authenticate_user_rejects_wrong_password(db_session):
    _seed(db_session)

    assert authenticate_user(db_session, "johndoe", "wrong") is None


def test_authenticate_user_rejects_unknown_user(db_session):
    assert authenticate_user(db_session, "ghost", "secret") is None
