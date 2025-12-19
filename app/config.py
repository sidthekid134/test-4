from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Story API"
    database_url: str = "sqlite:///./story.db"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()