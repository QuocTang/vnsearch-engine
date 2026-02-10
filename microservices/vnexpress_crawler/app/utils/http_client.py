"""HTTP Client utility"""

import requests
import logging
from typing import Optional, Dict, Any
from config import settings

logger = logging.getLogger(__name__)


class HttpClient:
    """HTTP client for making requests"""
    
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Referer": "https://vnexpress.net/",
    }
    
    @staticmethod
    def get(
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> requests.Response:
        """Make GET request"""
        
        timeout = timeout or settings.REQUEST_TIMEOUT
        headers = {**HttpClient.DEFAULT_HEADERS, **(headers or {})}
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"HTTP request failed: {url} - {str(e)}")
            raise
    
    @staticmethod
    def get_json(
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make GET request and return JSON"""
        response = HttpClient.get(url, params, headers)
        return response.json()
    
    @staticmethod
    def get_text(
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """Make GET request and return text (for HTML scraping)"""
        response = HttpClient.get(url, params, headers)
        return response.text
