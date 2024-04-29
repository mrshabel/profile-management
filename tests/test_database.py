import pytest
from httpx import AsyncClient
from databases import Database
from src.config import AppConfig

db = Database(AppConfig.DATABASE_URL.value)
