"""Comment models"""

from pydantic import BaseModel
from typing import Optional, List


class Comment(BaseModel):
    """Comment model"""
    id: Optional[str] = None
    author: str
    content: str
    created_at: Optional[str] = None
    likes: int = 0


class CommentsResponse(BaseModel):
    """Comments response"""
    status: str = "success"
    total: int
    limit: int
    offset: int
    data: List[Comment]
