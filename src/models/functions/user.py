from ..database import db
from ..tables.user import UsersTable
from src.schemas.user import UserSchema, UserSignUp
from sqlalchemy.sql.expression import (
    Insert as InsertQuery, Select as SelectQuery)
from datetime import datetime, timezone

# get user


async def get_user(id: str) -> UserSchema:
    """
    `Returns`: None if no user found
    """
    query: SelectQuery = UsersTable.select().where(UsersTable.c.id == id)
    user = await db.fetch_one(query=query)
    if not user:
        return None
    return UserSchema(**user)

# create user


async def create_user(data: UserSignUp) -> UserSchema:
    now = datetime.now(timezone.utc)

    query: InsertQuery = UsersTable.insert().values(
        **vars(data), created_at=now, updated_at=now)
    record_id = await db.execute(query=query)
    print(record_id)

    return UserSchema(id=record_id, **data.model_dump(), created_at=now, updated_at=now)

# update user

# delete user
