from fastapi import APIRouter, HTTPException, status
from fastapi.logger import logger
from src.models.functions.user import create_user, get_user
from src.schemas.user import UserSignUp, SuccessResponse
from asyncpg.exceptions import UniqueViolationError

router = APIRouter()


@router.post("/", response_model=SuccessResponse)
async def sign_up(req_data: UserSignUp):
    try:
        user = await create_user(req_data)
    except UniqueViolationError as e:
        logger.error("Duplicate key error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    except Exception as e:
        logger.error("Fatal Error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")

    return SuccessResponse(message="Sign up successfully", data=user)


@router.get("/{id}", response_model=SuccessResponse)
async def get_one_user(id: str):
    try:
        user = await get_user(id)
    except Exception as e:
        logger.error("Fatal error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return SuccessResponse(message="Successfully retrieved user", data=user)
