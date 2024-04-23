import dotenv
import os
from enum import Enum


dotenv.load_dotenv(".env")


class AppConfig(Enum):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    JWT_SECRET: str = os.environ["JWT_SECRET"]
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: str = os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"]
