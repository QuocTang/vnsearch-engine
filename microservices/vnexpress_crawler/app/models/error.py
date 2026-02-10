"""Error response model"""

from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """Error response"""
    status: str = "error"
    message: str
    error_code: Optional[str] = None
