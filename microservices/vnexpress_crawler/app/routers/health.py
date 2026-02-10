"""Health check router"""

from fastapi import APIRouter
from datetime import datetime
from app.models import HealthResponse
from config import settings

router = APIRouter(
    tags=["health"],
)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.utcnow().isoformat(),
    )
