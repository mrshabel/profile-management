import pytest
from httpx import AsyncClient
from src.main import app
from tests.test_database import db
from contextlib import asynccontextmanager


@pytest.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app):
        try:
            await db.connect()
            yield
        except Exception as e:
            await db.disconnect()
