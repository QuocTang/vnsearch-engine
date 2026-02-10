"""Configuration for VnExpress Crawler"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Config
    API_TITLE: str = "VnExpress Crawler API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # VnExpress URLs
    VNEXPRESS_BASE_URL: str = "https://vnexpress.net"
    VNEXPRESS_MICROSERVICE_URL: str = "https://vnexpress.net/microservice"
    VNEXPRESS_GW_URL: str = "https://gw.vnexpress.net"
    
    # Request Config
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    
    # Cache Config (seconds)
    CACHE_CATEGORIES: int = 3600  # 1 hour
    CACHE_ARTICLES: int = 300     # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
