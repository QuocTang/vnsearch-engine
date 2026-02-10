"""Category lookup utility"""

import json
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class CategoryLookup:
    """Lookup category_id from category_url"""
    
    _cache = None
    
    @staticmethod
    def _get_json_path():
        """Get path to categories.json file"""
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "json",
            "categories.json"
        )
    
    @staticmethod
    def _load_categories():
        """Load categories from JSON file or fetch from service"""
        if CategoryLookup._cache is not None:
            return CategoryLookup._cache
        
        json_path = CategoryLookup._get_json_path()
        
        # Try to load from file first
        try:
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and isinstance(data, dict):
                        CategoryLookup._cache = data
                        logger.info(f"Loaded {len(data)} categories from {json_path}")
                        return CategoryLookup._cache
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to load categories from file: {str(e)}")
        
        # If file doesn't exist or is empty, fetch from service
        logger.info("Categories file not found or empty, fetching from CategoryService...")
        try:
            from app.services.category_service import CategoryService
            
            categories_obj = CategoryService.get_all_categories()
            
            # Convert Category objects to dict for consistent format
            categories = {
                cat_id: {
                    "id": cat.id,
                    "url": cat.url,
                    "name": cat.name,
                    "parent_id": getattr(cat, 'parent_id', None)
                }
                for cat_id, cat in categories_obj.items()
            }
            
            # Save to file
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(categories, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(categories)} categories to {json_path}")
            CategoryLookup._cache = categories
            return categories
        
        except Exception as e:
            logger.error(f"Failed to fetch categories from service: {str(e)}")
            return {}
    
    @staticmethod
    def get_category_id_by_url(category_url: str) -> Optional[str]:
        """
        Get category_id from category_url
        
        Examples:
        - "the-gioi" -> "1001002"
        - "/the-gioi" -> "1001002"
        - "thoi-su" -> "1001005"
        """
        # Normalize URL (remove leading slash)
        if category_url.startswith('/'):
            category_url = category_url[1:]
        
        categories = CategoryLookup._load_categories()
        
        # Search for matching URL
        for cat_id, cat_data in categories.items():
            if isinstance(cat_data, dict) and "url" in cat_data:
                cat_url = cat_data["url"]
                # Remove leading slash for comparison
                if cat_url.startswith('/'):
                    cat_url = cat_url[1:]
                
                if cat_url == category_url:
                    return cat_data.get("id")
        
        return None
    
    @staticmethod
    def get_category_name_by_url(category_url: str) -> Optional[str]:
        """Get category name from URL"""
        if category_url.startswith('/'):
            category_url = category_url[1:]
        
        categories = CategoryLookup._load_categories()
        
        for cat_id, cat_data in categories.items():
            if isinstance(cat_data, dict) and "url" in cat_data:
                cat_url = cat_data["url"]
                if cat_url.startswith('/'):
                    cat_url = cat_url[1:]
                
                if cat_url == category_url:
                    return cat_data.get("name")
        
        return None
