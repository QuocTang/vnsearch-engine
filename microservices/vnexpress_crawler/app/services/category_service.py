"""Category service for fetching categories"""

import logging
from typing import Dict, List
from config import settings
from app.models import Category
from app.utils.http_client import HttpClient
from app.utils.cache import cache

logger = logging.getLogger(__name__)


class CategoryService:
    """Service for fetching and processing categories"""
    
    CACHE_KEY = "vnexpress:categories"
    
    @staticmethod
    def get_all_categories() -> Dict[str, Category]:
        """Get all categories with caching"""
        
        # Check cache first
        cached = cache.get(CategoryService.CACHE_KEY)
        if cached:
            logger.info("Categories retrieved from cache")
            return cached
        
        try:
            # Fetch from API
            url = f"{settings.VNEXPRESS_MICROSERVICE_URL}/fc"
            data = HttpClient.get_json(url)
            
            # Convert to Category objects
            categories = {
                cat_id: Category(id=cat_id, **cat_data)
                for cat_id, cat_data in data.items()
            }
            
            # Cache result
            cache.set(
                CategoryService.CACHE_KEY,
                categories,
                ttl=settings.CACHE_CATEGORIES,
            )
            
            logger.info(f"Fetched {len(categories)} categories from API")
            return categories
        
        except Exception as e:
            logger.error(f"Failed to fetch categories: {str(e)}")
            raise
    
    @staticmethod
    def get_category_by_id(category_id: str) -> Category:
        """Get a specific category by ID"""
        categories = CategoryService.get_all_categories()
        
        if category_id not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        return categories[category_id]
    
    @staticmethod
    def search_categories(query: str) -> List[Category]:
        """Search categories by name"""
        categories = CategoryService.get_all_categories()
        
        query_lower = query.lower()
        results = [
            cat for cat in categories.values()
            if query_lower in cat.name.lower()
        ]
        
        return results
