"""
IRS API - FastAPI Application
Information Retrieval System for Vietnamese articles using Vector Space Model.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1 import health, search, ingest
from app.core.config import get_settings
from app.api.v1.dependencies import get_tfidf_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to load TF-IDF model on startup.
    """
    logger.info("Starting IRS API...")
    
    # Load TF-IDF model on startup
    try:
        tfidf_service = get_tfidf_service()
        if tfidf_service.is_fitted:
            logger.info(f"✅ TF-IDF model loaded successfully")
            logger.info(f"   Vector dimension: {tfidf_service.get_vector_dimension()}")
        else:
            logger.warning("⚠️  TF-IDF model not found. Run ingestion first.")
    except Exception as e:
        logger.error(f"❌ Error loading TF-IDF model: {e}")
    
    yield
    
    logger.info("Shutting down IRS API...")


# Create FastAPI app
app = FastAPI(
    title="IRS API",
    description="Information Retrieval System API for Vietnamese articles using Vector Space Model",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(ingest.router, prefix="/api/v1", tags=["Admin"])


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
