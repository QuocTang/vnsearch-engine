"""Category models"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict


class Category(BaseModel):
    """Category model"""
    id: str
    url: str = Field(alias="u", description="Category URL slug")
    name: str = Field(alias="n", description="Category name")
    parent_id: Optional[int] = Field(None, alias="l", description="Parent category ID")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "1001005",
                "url": "/thoi-su",
                "name": "Thời sự",
                "parent_id": None
            }
        }
    )


class CategoryResponse(BaseModel):
    """Category response - uses full field names"""
    id: str
    url: str
    name: str
    parent_id: Optional[int] = None
    
    @classmethod
    def from_category(cls, cat: Category):
        """Convert Category to CategoryResponse"""
        return cls(
            id=cat.id,
            url=cat.url,
            name=cat.name,
            parent_id=cat.parent_id
        )


class CategoriesResponse(BaseModel):
    """Categories response"""
    status: str = "success"
    total: int
    data: Dict[str, CategoryResponse]
