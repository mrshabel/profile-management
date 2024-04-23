from fastapi import FastAPI
from src.routers import health_check, user, profile, auth
from src.models.database import db
from contextlib import asynccontextmanager


# define context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to the database when the server starts"""
    await db.connect()
    yield
    await db.disconnect()


# create application server instance
app = FastAPI(lifespan=lifespan, title="Profile Management Application")


app.include_router(health_check.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
