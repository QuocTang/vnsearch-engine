"""
Dependencies for API endpoints.
"""

from functools import lru_cache
from app.services.tfidf_service import TFIDFService
from app.services.nlp_processor import create_nlp_processor
from app.utils.stopwords_loader import load_stopwords
from app.core.config import get_settings


@lru_cache()
def get_tfidf_service() -> TFIDFService:
    """
    Get cached TF-IDF service instance with loaded model.
    
    Returns:
        TFIDFService: Loaded TF-IDF service
    """
    settings = get_settings()
    tfidf_service = TFIDFService()
    
    # Load model if exists
    try:
        tfidf_service.load(settings.tfidf_model_path)
    except FileNotFoundError:
        pass  # Model will be loaded after first ingestion
    
    return tfidf_service


@lru_cache()
def get_nlp_processor():
    """
    Get cached NLP processor instance.
    
    Returns:
        NLPProcessor: NLP processor with stopwords
    """
    settings = get_settings()
    stopwords = load_stopwords(settings.stopwords_path)
    return create_nlp_processor(stopwords)
