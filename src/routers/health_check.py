from fastapi import APIRouter

router = APIRouter(tags=["Health Check Endpoint"], prefix="/health-check")


@router.get("")
async def check_health():
    """Checks whether APIs are accessible from your query endpoint"""
    return "Great! Profile Management Service is Online"
