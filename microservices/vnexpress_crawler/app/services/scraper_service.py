"""Scraper service for VnExpress web pages"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import re
from bs4 import BeautifulSoup
from config import settings
from app.models import Article
from app.utils.http_client import HttpClient
from app.utils.cache import cache
import time

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for scraping VnExpress articles with pagination"""
    
    BASE_URL = "https://vnexpress.net"
    
    @staticmethod
    def get_articles_by_category_paginated(
        category_url: str,
        page: int = 1,
        category_id: Optional[str] = None
    ) -> List[Article]:
        """
        Scrape articles from category page with pagination
        
        Parameters:
        - category_url: Category URL slug (e.g., "/the-gioi")
        - page: Page number (1, 2, 3, etc.)
        - category_id: Category ID for metadata
        
        Returns: List of Article objects
        """
        cache_key = f"vnexpress:scraped:{category_url}:page{page}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Scraped articles from {category_url} page {page} retrieved from cache")
            return cached
        
        try:
            # Build URL with pagination
            if page == 1:
                url = f"{ScraperService.BASE_URL}{category_url}"
            else:
                url = f"{ScraperService.BASE_URL}{category_url}-p{page}"
            
            logger.info(f"Scraping {url}")
            
            # Fetch page
            html = HttpClient.get_text(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            articles = []
            
            # Find article containers - VnExpress uses article items in specific divs
            article_items = soup.find_all('article', class_='item-news')
            
            if not article_items:
                # Fallback: try another selector
                article_items = soup.find_all('div', class_='item-news')
            
            for item in article_items:
                try:
                    # Extract title and URL
                    title_elem = item.find('a', class_='title-news')
                    if not title_elem:
                        title_elem = item.find('h3', class_='title-news')
                        if title_elem:
                            title_elem = title_elem.find('a')
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    if not url:
                        continue
                    
                    # Make URL absolute
                    if url.startswith('/'):
                        url = ScraperService.BASE_URL + url
                    elif not url.startswith('http'):
                        url = ScraperService.BASE_URL + '/' + url
                    
                    # Extract article ID from URL
                    article_id = ScraperService._extract_article_id(url)
                    
                    # Extract summary/description
                    desc_elem = item.find('p', class_='description')
                    summary = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract thumbnail (handle lazy loading with data-src)
                    img_elem = item.find('img')
                    thumbnail_url = ""
                    if img_elem:
                        # Ưu tiên data-src (lazy load), sau đó src
                        thumbnail_url = img_elem.get('data-src', '') or img_elem.get('src', '')
                        
                        # Nếu vẫn không có, thử lấy từ srcset trong <picture>
                        if not thumbnail_url:
                            picture = item.find('picture')
                            if picture:
                                source = picture.find('source')
                                if source:
                                    srcset = source.get('data-srcset', '') or source.get('srcset', '')
                                    # Lấy URL đầu tiên từ srcset
                                    if srcset:
                                        thumbnail_url = srcset.split()[0]
                    
                    # Extract publish time
                    time_elem = item.find('span', class_='publishtime')
                    published_at = None
                    if time_elem:
                        time_str = time_elem.get('data-publish-time', '')
                        if time_str:
                            try:
                                published_at = datetime.fromtimestamp(int(time_str)).isoformat()
                            except (ValueError, TypeError):
                                published_at = time_elem.get_text(strip=True)
                    
                    article = Article(
                        id=article_id,
                        title=title,
                        url=url,
                        summary=summary,
                        thumbnail_url=thumbnail_url,
                        published_at=published_at,
                        category_id=category_id,
                    )
                    articles.append(article)
                
                except Exception as e:
                    logger.warning(f"Failed to parse article item: {str(e)}")
                    continue
            
            # Cache result
            cache.set(cache_key, articles, ttl=settings.CACHE_ARTICLES)
            
            logger.info(f"Scraped {len(articles)} articles from {category_url} page {page}")
            return articles
        
        except Exception as e:
            logger.error(f"Failed to scrape {category_url} page {page}: {str(e)}")
            raise
    
    @staticmethod
    def get_articles_paginated(
        category_url: str,
        limit: int = 20,
        page: int = 1,
        category_id: Optional[str] = None
    ) -> List[Article]:
        """
        Get articles with pagination support
        
        Parameters:
        - category_url: Category URL slug
        - limit: Number of articles per page
        - page: Page number
        - category_id: Category ID
        
        Returns: Limited list of articles
        """
        articles = ScraperService.get_articles_by_category_paginated(
            category_url=category_url,
            page=page,
            category_id=category_id
        )
        
        # Limit results
        return articles[:limit]
    
    @staticmethod
    def get_articles_by_date_range(
        category_id: str,
        from_date: int,
        to_date: int,
        page: int = 1,
        limit: int = 50,
        category_url: Optional[str] = None
    ) -> List[Article]:
        """
        Scrape articles by category and date range with pagination
        
        Parameters:
        - category_id: Category ID (e.g., "1001002")
        - from_date: Unix timestamp for start date
        - to_date: Unix timestamp for end date
        - page: Page number (1, 2, 3, etc.)
        - limit: Max articles to return
        - category_url: Category URL slug (optional, used for display)
        
        Returns: List of Article objects
        """
        cache_key = f"vnexpress:scraped:date:{category_id}:{from_date}:{to_date}:page{page}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Scraped articles for category {category_id} from date range page {page} retrieved from cache")
            return cached[:limit]
        
        try:
            # Build URL with date range and pagination
            if page == 1:
                url = (
                    f"{ScraperService.BASE_URL}/category/day/cateid/{category_id}"
                    f"/fromdate/{from_date}/todate/{to_date}/allcate/{category_id}"
                )
            else:
                url = (
                    f"{ScraperService.BASE_URL}/category/day/cateid/{category_id}"
                    f"/fromdate/{from_date}/todate/{to_date}/allcate/{category_id}/page/{page}"
                )
            
            logger.info(f"Scraping {url}")
            
            # Fetch page
            html = HttpClient.get_text(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            articles = []
            
            # Find article containers
            article_items = soup.find_all('article', class_='item-news')
            
            if not article_items:
                # Fallback: try another selector
                article_items = soup.find_all('div', class_='item-news')
            
            for item in article_items:
                if len(articles) >= limit:
                    break
                
                try:
                    # Extract title and URL
                    title_elem = item.find('a', class_='title-news')
                    if not title_elem:
                        title_elem = item.find('h3', class_='title-news')
                        if title_elem:
                            title_elem = title_elem.find('a')
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    if not url:
                        continue
                    
                    # Make URL absolute
                    if url.startswith('/'):
                        url = ScraperService.BASE_URL + url
                    elif not url.startswith('http'):
                        url = ScraperService.BASE_URL + '/' + url
                    
                    # Extract article ID from URL
                    article_id = ScraperService._extract_article_id(url)
                    
                    # Extract summary/description
                    desc_elem = item.find('p', class_='description')
                    summary = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract thumbnail (handle lazy loading with data-src)
                    img_elem = item.find('img')
                    thumbnail_url = ""
                    if img_elem:
                        # Ưu tiên data-src (lazy load), sau đó src
                        thumbnail_url = img_elem.get('data-src', '') or img_elem.get('src', '')
                        
                        # Nếu vẫn không có, thử lấy từ srcset trong <picture>
                        if not thumbnail_url:
                            picture = item.find('picture')
                            if picture:
                                source = picture.find('source')
                                if source:
                                    srcset = source.get('data-srcset', '') or source.get('srcset', '')
                                    # Lấy URL đầu tiên từ srcset
                                    if srcset:
                                        thumbnail_url = srcset.split()[0]
                    
                    # Extract publish time
                    time_elem = item.find('span', class_='publishtime')
                    published_at = None
                    if time_elem:
                        time_str = time_elem.get('data-publish-time', '')
                        if time_str:
                            try:
                                published_at = datetime.fromtimestamp(int(time_str)).isoformat()
                            except (ValueError, TypeError):
                                published_at = time_elem.get_text(strip=True)
                    
                    article = Article(
                        id=article_id,
                        title=title,
                        url=url,
                        summary=summary,
                        thumbnail_url=thumbnail_url,
                        published_at=published_at,
                        category_id=category_id,
                    )
                    articles.append(article)
                
                except Exception as e:
                    logger.warning(f"Failed to parse article item: {str(e)}")
                    continue
            
            # Cache result
            cache.set(cache_key, articles, ttl=settings.CACHE_ARTICLES)
            
            logger.info(f"Scraped {len(articles)} articles for category {category_id} in date range")
            return articles
        
        except Exception as e:
            logger.error(f"Failed to scrape category {category_id} by date: {str(e)}")
            raise
    
    @staticmethod
    def get_articles_by_date_range_str(
        category_id: str,
        from_date: str,
        to_date: str,
        page: int = 1,
        category_url: Optional[str] = None
    ) -> List[Article]:
        """
        Scrape articles by category and date range using string dates
        
        Parameters:
        - category_id: Category ID (e.g., "1001002")
        - from_date: Start date as string (YYYY-MM-DD)
        - to_date: End date as string (YYYY-MM-DD)
        - page: Page number (1, 2, 3, etc.)
        - category_url: Category URL slug (optional)
        
        Returns: List of Article objects for specified page
        """
        try:
            # Parse date strings to Unix timestamps
            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
            to_dt = datetime.strptime(to_date, "%Y-%m-%d")
            
            # Validate date range
            if from_dt > to_dt:
                raise ValueError(f"from_date ({from_date}) cannot be after to_date ({to_date})")
            
            # Check if from_date is in the future
            if from_dt > datetime.now():
                raise ValueError(f"from_date ({from_date}) cannot be in the future")
            
            # Check date range limit (100 days max)
            date_range_days = (to_dt - from_dt).days
            max_days = 100
            if date_range_days > max_days:
                raise ValueError(f"Date range cannot exceed {max_days} days. Your range: {date_range_days} days ({from_date} to {to_date})")
            
            # Convert to timestamps
            from_ts = int(from_dt.timestamp())
            to_ts = int(to_dt.timestamp())
            
            # Add 1 day to to_date to include entire day
            to_ts += 86400
            
            logger.info(f"Date range: {from_date} to {to_date} ({date_range_days} days), Unix: {from_ts} to {to_ts}")
            
            return ScraperService.get_articles_by_date_range(
                category_id=category_id,
                from_date=from_ts,
                to_date=to_ts,
                page=page,
                limit=50,
                category_url=category_url,
            )
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")
            raise
    
    @staticmethod
    def _extract_article_id(url: str) -> str:
        """Extract article ID from VnExpress URL"""
        # VnExpress URL format: https://vnexpress.net/...article-slug-123456.html
        # Article ID is the number before .html
        match = re.search(r'-(\d+)\.html', url)
        if match:
            return match.group(1)
        
        # Fallback: use URL hash
        return str(hash(url))
