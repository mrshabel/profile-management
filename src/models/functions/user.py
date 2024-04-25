from ..database import db
from ..tables.user import UsersTable
from src.schemas.user import UserSchema
from sqlalchemy.sql.expression import (
    Insert as InsertQuery, Select as SelectQuery)


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


# update user

# delete user
