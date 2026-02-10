"""Health check model"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    timestamp: str
