from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi.logger import logger
from typing import Annotated
from datetime import datetime, timedelta, timezone
from src.config import AppConfig
from src.schemas.auth import TokenData, UserSignUp, UserData
from src.models.tables.user import UsersTable
from ..database import db
from sqlalchemy.sql.expression import Insert as InsertQuery, Select as SelectQuery
from asyncpg.exceptions import UniqueViolationError


auth_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Returns a boolean indicating whether password is valid or not
    """
    return auth_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Returns a hash of the password
    """
    return auth_context.hash(password)


def create_access_token(payload: dict) -> str:
    """
    `Args`: payload
    `Returns`: Access token of the user
    """
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=float(AppConfig.JWT_ACCESS_TOKEN_EXPIRES_MINUTES.value)
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, AppConfig.JWT_SECRET.value, algorithm="HS256")
    return token


async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> UserData | None:
    query: SelectQuery = UsersTable.select().where(
        UsersTable.c.username == form_data.username
    )
    user = await db.fetch_one(query)

    if not user:
        return None

    return UserData(**user)


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenData:
    user = await login_user(form_data)
    if not user:
        logger.error("Fatal error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    token = create_access_token({"id": str(user.id)})
    return TokenData(token)


async def signup_user(req_data: UserSignUp) -> str:
    now = datetime.now(timezone.utc)
    hashed_password = get_password_hash(req_data.password)
    req_data.password = hashed_password

    query: InsertQuery = UsersTable.insert().values(
        **req_data.model_dump(), created_at=now, updated_at=now
    )
    record_id = await db.execute(query=query)

    return record_id
