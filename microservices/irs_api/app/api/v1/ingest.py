"""
Ingest endpoint - Trigger data ingestion pipeline.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.response import IngestResponse
from app.services.ingestion_service import IngestionService

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse, tags=["Admin"])
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Trigger data ingestion pipeline.
    
    This endpoint runs the full ingestion process:
    1. Load Excel data
    2. Preprocess with NLP
    3. Train TF-IDF model
    4. Transform to vectors
    5. Index to Qdrant
    
    Note: This is a long-running operation and may take 30+ seconds.
    
    Returns:
        IngestResponse: Ingestion statistics
    """
    try:
        # Run ingestion synchronously (for simplicity)
        # In production, consider using background_tasks or async workers
        ingestion_service = IngestionService()
        stats = ingestion_service.run_full_ingestion()
        
        return IngestResponse(
            status=stats["status"],
            articles_count=stats["articles_count"],
            vector_dimension=stats["vector_dimension"],
            qdrant_collection=stats["qdrant_collection"],
            qdrant_points=stats["qdrant_points"],
            categories=stats["categories"],
            model_path=stats["model_path"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi ingest data: {str(e)}"
        )
