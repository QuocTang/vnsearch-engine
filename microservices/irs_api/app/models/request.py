"""
Request models for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SearchRequest(BaseModel):
    """Search request model."""
    
    query: str = Field(
        ...,
        description="Search query in Vietnamese",
        min_length=1,
        max_length=500,
        examples=["công nghệ trí tuệ nhân tạo"]
    )
    
    limit: int = Field(
        default=10,
        description="Number of results to return",
        ge=1,
        le=100
    )
    
    category_filter: Optional[str] = Field(
        default=None,
        description="Filter by category name",
        examples=["Khoa học", "Công nghệ"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "công nghệ trí tuệ nhân tạo",
                "limit": 10,
                "category_filter": "Khoa học"
            }
        }
