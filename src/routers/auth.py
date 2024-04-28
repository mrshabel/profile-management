from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.auth import (
    SuccessResponseForLogin,
    SuccessResponseForSignup,
    UserSignUp,
)
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg.exceptions import UniqueViolationError
from src.models.functions.auth import (
    login_user,
    create_access_token,
    signup_user,
    verify_password,
)

router = APIRouter(tags=["Authentication Endpoints"])


@router.post("/login", response_model=SuccessResponseForLogin)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await login_user(form_data=form_data)
    except BaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login user",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # verify user password
    is_valid_user = verify_password(form_data.password, user.password)
    if not is_valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"id": str(user.id)})

    return SuccessResponseForLogin(message="Login successful", data=user, token=token)


@router.post("/signup", response_model=SuccessResponseForSignup)
async def signup(req_data: UserSignUp):
    try:
        await signup_user(req_data=req_data)
    except UniqueViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    except BaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add user",
        )
    return SuccessResponseForSignup(message="Signup successful")
