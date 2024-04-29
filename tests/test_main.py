import pytest
import pytest_asyncio
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app
from tests.test_database import db
from contextlib import asynccontextmanager


@pytest_asyncio.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app):
        try:
            await db.connect()
            yield
        except Exception as e:
            await db.disconnect()
