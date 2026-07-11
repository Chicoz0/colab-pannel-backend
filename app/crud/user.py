from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserInDB


def get_user(db: Session, username: str) -> UserInDB | None:
    row = db.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()
    if row is None:
        return None
    return UserInDB.model_validate(row)
