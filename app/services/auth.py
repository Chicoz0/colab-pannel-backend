from sqlalchemy.orm import Session

from app.core.security import DUMMY_HASH, verify_password
from app.crud.user import get_user
from app.schemas.user import UserInDB


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | None:
    user = get_user(db, username)
    if user is None:
        # Hash a throwaway password so a missing user costs the same time as a
        # wrong password (defends against username-enumeration by timing).
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
