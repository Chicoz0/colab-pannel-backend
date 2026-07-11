from pathlib import Path

from pydantic_settings import BaseSettings

# This file lives at backend/app/core/config.py, so three parents up is backend/,
# where .env and alembic.ini live.
ROOT = Path(__file__).resolve().parent.parent.parent


# Map .env variables to settings attributes.
class Settings(BaseSettings):
    model_config = {
        "env_file": ROOT / ".env",
        "env_file_encoding": "utf-8",
    }

    database_url: str
    test_database_url: str
    secret_key: str


settings = Settings()  # pyright: ignore[reportCallIssue]
