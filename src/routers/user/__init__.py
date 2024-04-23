from fastapi import APIRouter
from . import add_one_user

router = APIRouter(tags=["User Endpoints"], prefix="/user")

# define router functions here
router.include_router(add_one_user.router)
