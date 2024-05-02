from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import health_check, user, profile, auth
from src.models.database import db
from contextlib import asynccontextmanager
from src.middlewares import db_exceptions


# define context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to the database when the server starts"""
    await db.connect()
    yield
    await db.disconnect()


# create application server instance
app = FastAPI(
    lifespan=lifespan,
    title="Profile Management Application",
    description="An application for managing user personal information and profiles",
)

# add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""],
)
# app.exception_handler
app.middleware("http")(db_exceptions.db_exceptions_handler)


app.include_router(health_check.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
