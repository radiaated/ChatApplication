from pydantic_settings import BaseSettings

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")
    # In seconds
    JWT_EXPIRES_IN: int = 900


# Singleton settings instance
settings = Settings()
