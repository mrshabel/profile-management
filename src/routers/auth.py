from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.auth import SuccessResponseForLogin
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.models.functions.auth import login_user, create_access_token

router = APIRouter(tags=["Authentication Endpoints"])


@router.post("/login", response_model=SuccessResponseForLogin)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await login_user(form_data=form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    token = create_access_token(id=user.id)

    return SuccessResponseForLogin(**user._mapping, token=token)
