"""
Response models for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    model_loaded: bool = Field(..., description="TF-IDF model loaded status")
    

class ArticleResult(BaseModel):
    """Single article search result."""
    
    id: int = Field(..., description="Point ID in Qdrant")
    score: float = Field(..., description="Similarity score (0-1)")
    article_id: int = Field(..., description="Original article ID")
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="Article summary")
    url: str = Field(..., description="Article URL")
    category_name: str = Field(..., description="Category name")
    comment_count: int = Field(..., description="Number of comments")


class SearchResponse(BaseModel):
    """Search results response."""
    
    query: str = Field(..., description="Original search query")
    processed_query: str = Field(..., description="Preprocessed query")
    total_results: int = Field(..., description="Number of results returned")
    results: List[ArticleResult] = Field(..., description="List of article results")
    execution_time_ms: float = Field(..., description="Search execution time in milliseconds")
    

class IngestResponse(BaseModel):
    """Ingestion response."""
    
    status: str = Field(..., description="Ingestion status")
    articles_count: int = Field(..., description="Number of articles indexed")
    vector_dimension: int = Field(..., description="Vector dimension")
    qdrant_collection: str = Field(..., description="Qdrant collection name")
    qdrant_points: int = Field(..., description="Number of points in Qdrant")
    categories: int = Field(..., description="Number of unique categories")
    model_path: str = Field(..., description="Path to saved model")
