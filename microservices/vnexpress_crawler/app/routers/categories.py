"""Categories router"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging

from app.models import Category, CategoryResponse, CategoriesResponse, ErrorResponse
from app.services.category_service import CategoryService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["categories"])


@router.get("/", response_model=CategoriesResponse)
async def get_all_categories() -> CategoriesResponse:
    """
    Get all VnExpress categories
    
    Returns all available categories with their metadata
    """
    try:
        categories = CategoryService.get_all_categories()
        # Convert Category to CategoryResponse
        response_data = {
            cat_id: CategoryResponse.from_category(cat)
            for cat_id, cat in categories.items()
        }
        return CategoriesResponse(
            total=len(response_data),
            data=response_data,
        )
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")


@router.get("/search")
async def search_categories(q: str = Query(..., min_length=1)):
    """
    Search categories by name
    
    Parameters:
    - q: Search query
    
    Example: /api/v1/categories/search?q=thoi
    """
    try:
        results = CategoryService.search_categories(q)
        # Convert to response format
        response_data = [CategoryResponse.from_category(cat) for cat in results]
        return {
            "status": "success",
            "total": len(response_data),
            "query": q,
            "data": response_data,
        }
    except Exception as e:
        logger.error(f"Error searching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search categories")


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str) -> CategoryResponse:
    """
    Get a specific category by ID
    
    Parameters:
    - category_id: Category ID (e.g., "1001005")
    """
    try:
        category = CategoryService.get_category_by_id(category_id)
        return CategoryResponse.from_category(category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch category")
