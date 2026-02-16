"""
Health check endpoint.
"""

from fastapi import APIRouter, Depends
from app.models.response import HealthResponse
from app.core.config import get_settings
from app.services.qdrant_service import QdrantService
from app.api.v1.dependencies import get_tfidf_service

router = APIRouter()


@router.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check(
    tfidf_service = Depends(get_tfidf_service)
):
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service health status
    """
    settings = get_settings()
    
    # Check Qdrant connection
    qdrant = QdrantService(settings.qdrant_host, settings.qdrant_port)
    qdrant_connected = qdrant.health_check()
    
    # Check TF-IDF model loaded
    model_loaded = tfidf_service.is_fitted
    
    return HealthResponse(
        status="healthy" if (qdrant_connected and model_loaded) else "degraded",
        qdrant_connected=qdrant_connected,
        model_loaded=model_loaded
    )
