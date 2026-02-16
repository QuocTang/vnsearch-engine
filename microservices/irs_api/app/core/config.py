"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "articles"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Data Paths
    excel_articles_path: str = "assets/excel/articles.xlsx"
    excel_categories_path: str = "assets/excel/categories.xlsx"
    excel_comments_path: str = "assets/excel/comments.xlsx"
    stopwords_path: str = "assets/txt/vietnamese-stopwords.txt"
    
    # Model Paths
    tfidf_model_path: str = "models/tfidf_vectorizer.pkl"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings singleton
    """
    return Settings()
