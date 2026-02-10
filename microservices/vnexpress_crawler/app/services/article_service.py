"""Article service for fetching articles and comments"""

import logging
from typing import List, Dict, Any, Optional
from config import settings
from app.models import Article, Comment
from app.utils.http_client import HttpClient
from app.utils.cache import cache

logger = logging.getLogger(__name__)


class ArticleService:
    """Service for fetching articles and comments"""
    
    COMMENTS_API = "https://usi-saas.vnexpress.net/index/get"
    
    @staticmethod
    def get_articles_by_category(
        category_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Article]:
        """
        Get articles by category using VnExpress GW API
        
        Note: Uses gw.vnexpress.net/bt endpoint which provides article data
        """
        cache_key = f"vnexpress:articles:{category_id}:{offset}:{limit}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Articles for category {category_id} retrieved from cache")
            return cached
        
        try:
            api_url = "https://gw.vnexpress.net/bt"
            params = {
                "site_id": 1000000,
                "category_id": category_id,
                "showed_area": f"doanhnghiep:{limit}",
                "limit": limit,
                "data_select": "article_id,title,share_url,thumbnail_url,publish_time,lead"
            }
            
            response = HttpClient.get_json(api_url, params=params)
            
            articles = []
            if response.get("code") == 200 and response.get("data"):
                # Parse articles from different sections
                data = response.get("data", {})
                global_idx = 0  # Track index across all sections
                for section_name, section_data in data.items():
                    if isinstance(section_data, dict) and "data" in section_data:
                        for item in section_data["data"]:
                            if len(articles) >= limit:
                                break
                            
                            # Skip items before offset
                            if global_idx < offset:
                                global_idx += 1
                                continue
                            
                            global_idx += 1
                            
                            # Convert Unix timestamp to ISO format
                            publish_time = item.get("publish_time")
                            published_at = None
                            if publish_time:
                                from datetime import datetime
                                published_at = datetime.utcfromtimestamp(publish_time).isoformat()
                            
                            article = Article(
                                id=str(item.get("article_id")),
                                title=item.get("title", ""),
                                url=item.get("share_url", ""),
                                summary=item.get("lead", ""),
                                thumbnail_url=item.get("thumbnail_url", ""),
                                published_at=published_at,
                                category_id=category_id,
                            )
                            articles.append(article)
            
            # Cache result
            cache.set(cache_key, articles, ttl=settings.CACHE_ARTICLES)
            
            logger.info(f"Fetched {len(articles)} articles from category {category_id}")
            return articles
        
        except Exception as e:
            logger.error(f"Failed to fetch articles: {str(e)}")
            raise
    
    @staticmethod
    def get_article_by_id(article_id: str) -> Optional[Article]:
        """
        Get article details by ID
        
        Note: Requires article object ID and type to fetch comments/reactions
        """
        cache_key = f"vnexpress:article:{article_id}"
        
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Article {article_id} retrieved from cache")
            return cached
        
        try:
            # VnExpress doesn't provide a public article detail API
            logger.warning(f"Article detail not available for {article_id}")
            return None
        
        except Exception as e:
            logger.error(f"Failed to fetch article {article_id}: {str(e)}")
            raise
    
    @staticmethod
    def get_article_comments(
        article_id: str,
        object_id: str,
        object_type: int = 1,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "like"
    ) -> List[Comment]:
        """
        Get comments for an article using VnExpress Comment API
        
        Parameters:
        - article_id: VnExpress article ID
        - object_id: Comment object ID (required for API)
        - object_type: Type of object (1=article)
        - limit: Number of comments
        - offset: Pagination offset
        - sort_by: Sort order (like, newest, oldest)
        """
        cache_key = f"vnexpress:comments:{object_id}:{offset}:{limit}:{sort_by}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Comments for article {article_id} retrieved from cache")
            return cached
        
        try:
            params = {
                "offset": offset,
                "limit": limit,
                "frommobile": 0,
                "sort_by": sort_by,
                "is_onload": 0,
                "objectid": object_id,
                "objecttype": object_type,
                "siteid": 1000000,
            }
            
            response = HttpClient.get_json(ArticleService.COMMENTS_API, params=params)
            
            # Parse comments from response
            comments = []
            if response.get("error") == 0 and response.get("data"):
                items = response["data"].get("items", [])
                for item in items:
                    comment = Comment(
                        id=str(item.get("comment_id")),
                        author=item.get("full_name", "Unknown"),
                        content=item.get("content", ""),
                        created_at=item.get("time"),
                        likes=item.get("userlike", 0)
                    )
                    comments.append(comment)
            
            # Cache result
            cache.set(cache_key, comments, ttl=settings.CACHE_ARTICLES)
            
            logger.info(f"Fetched {len(comments)} comments for article {article_id}")
            return comments
        
        except Exception as e:
            logger.error(f"Failed to fetch comments for article {article_id}: {str(e)}")
            raise
