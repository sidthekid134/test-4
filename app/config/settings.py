import os
from pydantic import BaseSettings, validator
from typing import Optional


class Settings(BaseSettings):
    # Base settings
    APP_NAME: str = "test1"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./test1.db"
    
    # API settings
    API_PREFIX: str = "/api"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v, values):
        if v.startswith("sqlite"):
            return v
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()