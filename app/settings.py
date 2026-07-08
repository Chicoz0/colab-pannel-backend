from pathlib import Path

from pydantic_settings import BaseSettings

ROOT= Path(__file__).resolve().parent.parent

# Map .env variables to settings attributes.
class Settings(BaseSettings):
      model_config = {
          "env_file": ROOT / ".env",
          "env_file_encoding": "utf-8",
      }
      
      database_url: str
      test_database_url: str


settings = Settings() # pyright: ignore[reportCallIssue]
