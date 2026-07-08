from pathlib import Path

from pydantic_settings import BaseSettings

ROOT= Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
      model_config = {
          "env_file": ROOT / ".env",
          "env_file_encoding": "utf-8",
      }
      
      database_url: str


settings = Settings() # pyright: ignore[reportCallIssue]
