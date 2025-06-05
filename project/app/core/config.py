import os
from pydantic_settings import BaseSettings  # Изменено с pydantic импорта

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/db/app.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()