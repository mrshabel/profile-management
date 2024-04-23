from databases import Database
from src.config import AppConfig

db = Database(AppConfig.DATABASE_URL.value)
