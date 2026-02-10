"""Article models"""

from pydantic import BaseModel
from typing import Optional, List


class Article(BaseModel):
    """Article model"""
    id: Optional[str] = None
    title: str
    url: str
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    published_at: Optional[str] = None
    category_id: Optional[str] = None


class ArticlesResponse(BaseModel):
    """Articles response"""
    status: str = "success"
    total: int
    limit: int
    offset: int
    data: List[Article]
