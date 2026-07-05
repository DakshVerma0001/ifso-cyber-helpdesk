from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health Check",
)
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }