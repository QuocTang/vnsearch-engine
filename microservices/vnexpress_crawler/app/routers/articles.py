"""Articles router"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging

from app.models import Article, ArticlesResponse, Comment, CommentsResponse, ErrorResponse
from app.services.article_service import ArticleService
from app.services.scraper_service import ScraperService
from app.utils.category_lookup import CategoryLookup

logger = logging.getLogger(__name__)
router = APIRouter(tags=["articles"])


@router.get(
    "/category/{category_id}",
    response_model=ArticlesResponse,
    responses={500: {"model": ErrorResponse}},
)
async def get_articles_by_category(
    category_id: str,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
) -> ArticlesResponse:
    """
    Get articles by category
    
    Parameters:
    - category_id: Category ID (e.g., "1000000", "1001005")
    - limit: Number of articles (default: 20, max: 50)
        - offset: Offset for pagination (default: 0)
    
    Note: Uses VnExpress GW API (gw.vnexpress.net/bt) - Fast, no browser needed!
    """
    try:
        articles = ArticleService.get_articles_by_category(category_id, limit, offset)
        return ArticlesResponse(
            total=len(articles),
            limit=limit,
            offset=offset,
            data=articles,
        )
    except Exception as e:
        logger.error(f"Error fetching articles for category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch articles")


@router.get("/category-paginated/{category_url}", response_model=ArticlesResponse)
async def get_articles_by_category_paginated(
    category_url: str,
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    category_id: Optional[str] = None,
) -> ArticlesResponse:
    """
    Get articles by category with web scraping (supports real pagination)
    
    Parameters:
    - category_url: Category URL slug (e.g., "the-gioi", "thoi-su")
    - limit: Number of articles (default: 20, max: 100)
    - page: Page number (1, 2, 3, etc.) (default: 1)
    - category_id: Category ID (optional, will be looked up from URL if not provided)
    
    Example: /api/v1/articles/category-paginated/the-gioi?page=2&limit=20
    """
    try:
        # If category_id not provided, look it up from URL
        if not category_id:
            category_id = CategoryLookup.get_category_id_by_url(category_url)
        
        articles = ScraperService.get_articles_paginated(
            category_url=f"/{category_url}",
            limit=limit,
            page=page,
            category_id=category_id,
        )
        return ArticlesResponse(
            total=len(articles),
            limit=limit,
            offset=(page - 1) * limit,
            data=articles,
        )
    except Exception as e:
        logger.error(f"Error fetching articles for category {category_url} page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch articles")


@router.get("/category-date/{category_id}", response_model=ArticlesResponse)
async def get_articles_by_date_range(
    category_id: str,
    from_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> ArticlesResponse:
    """
    Get articles by category within date range with pagination
    
    Parameters:
    - category_id: Category ID (e.g., "1001002")
    - from_date: Start date (YYYY-MM-DD format, e.g., "2025-09-01")
    - to_date: End date (YYYY-MM-DD format, e.g., "2026-01-01")
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    
    Example: /api/v1/articles/category-date/1001002?from_date=2025-09-01&to_date=2026-01-01&page=1&limit=20
    """
    try:
        articles = ScraperService.get_articles_by_date_range_str(
            category_id=category_id,
            from_date=from_date,
            to_date=to_date,
            page=page,
        )
        
        # Calculate offset for response
        offset = (page - 1) * limit
        
        return ArticlesResponse(
            total=len(articles),
            limit=limit,
            offset=offset,
            data=articles,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching articles for category {category_id} by date: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch articles")


@router.get("/{article_id}/comments", response_model=CommentsResponse)
async def get_article_comments(
    article_id: str,
    object_id: str = Query(..., description="VnExpress comment object ID"),
    object_type: int = Query(1, description="Object type (1=article)"),
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1, description="Page number (default: 1)"),
    sort_by: str = Query("like", regex="^(like|newest|oldest)$"),
):
    """
    Get comments for an article using VnExpress Comment API
    
    Parameters:
    - article_id: Article ID
    - object_id: VnExpress comment object ID (required)
    - object_type: Object type (default: 1 for article)
    - limit: Number of comments (default: 20, max: 100)
    - page: Page number (default: 1)
    - sort_by: Sort order - like, newest, oldest (default: like)
    
    Example: /api/v1/articles/123/comments?object_id=4988419&limit=20&page=1
    """
    try:
        # Calculate offset from page and limit
        offset = (page - 1) * limit
        
        comments = ArticleService.get_article_comments(
            article_id=article_id,
            object_id=object_id,
            object_type=object_type,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
        )
        return CommentsResponse(
            total=len(comments),
            limit=limit,
            offset=offset,
            data=comments,
        )
    except Exception as e:
        logger.error(f"Error fetching comments for article {article_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch comments")
