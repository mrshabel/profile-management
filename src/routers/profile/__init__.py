from fastapi import APIRouter

router = APIRouter(tags=["Profile Endpoints"], prefix="/profile")

# router.include_router()