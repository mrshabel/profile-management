from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from typing import Annotated
from datetime import datetime, timedelta, timezone
from src.config import AppConfig
from src.schemas.auth import TokenData
from src.schemas.user import UserSchema, UserSignUp
from src.models.tables.user import UsersTable
from ..database import db
from sqlalchemy.sql.expression import (
    Insert as InsertQuery, Select as SelectQuery)


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


def create_access_token(payload: TokenData) -> str:
    """
    `Args`: payload
    `Returns`: Access token of the user
    """
    to_encode = payload.model_copy()
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=AppConfig.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, AppConfig.JWT_SECRET.value,
                       algorithms=["HS256"])
    return token


async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> UserSchema | None:
    try:
        query: SelectQuery = UsersTable.select().where(
            UsersTable.c.username == form_data.username)
        user = await db.fetch_one(query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to login user")
    if not user:
        return None

    is_valid_user = verify_password(form_data.password, user.password)
    if not is_valid_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    return UserSchema(**user._mapping)


async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenData:
    user = await login_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    token = create_access_token(id=user.id)
    return TokenData(token)


async def signup_user(req_data: UserSignUp) -> UserSchema:
    now = datetime.now(timezone.utc)
    hashed_password = get_password_hash(req_data.password)

    query: InsertQuery = UsersTable.insert().values(
        **vars(req_data), password=hashed_password, created_at=now, updated_at=now)
    record_id = await db.execute(query=query)
    print(record_id)

    return UserSchema(id=record_id, **req_data.model_dump(), created_at=now, updated_at=now)
