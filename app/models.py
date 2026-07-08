from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str | None]
    full_name: Mapped[str | None]
    disabled: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]
