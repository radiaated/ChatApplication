from pydantic_settings import BaseSettings

from dotenv import load_dotenv

import os

load_dotenv()


class Settings(BaseSettings):

    DATABASE_URL: str = os.environ.get("DATABASE_URL")


settings = Settings()
