"""
NLP Processor service for Vietnamese text.
Provides consistent text preprocessing for both ingestion and search.
"""

from typing import List
from underthesea import word_tokenize


class NLPProcessor:
    """
    Vietnamese NLP processor for text preprocessing.
    CRITICAL: Ensure consistent preprocessing between ingestion and search.
    """
    
    def __init__(self, stopwords: set[str]):
        """
        Initialize NLP processor with stopwords.
        
        Args:
            stopwords: Set of Vietnamese stopwords to remove
        """
        self.stopwords = stopwords
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess Vietnamese text with consistent pipeline.
        
        Pipeline:
        1. Tokenize using underthesea.word_tokenize()
        2. Lowercase normalization
        3. Remove stopwords
        
        Args:
            text: Raw Vietnamese text
            
        Returns:
            str: Preprocessed text (space-separated tokens)
        """
        if not text or not text.strip():
            return ""
        
        # Step 1: Tokenize Vietnamese text
        tokens = word_tokenize(text, format="text")

        
        # Step 2: Split tokens, lowercase, and normalize compound words
        # Replace underscores (underthesea compound markers) with spaces so that
        # "công_nghệ_thông_tin" (query) and "công_nghệ thông_tin" (document) produce
        # the same individual tokens, avoiding tokenization inconsistency.
        words = tokens.lower().replace('_', ' ').split()
        
        # Step 3: Remove stopwords
        filtered_words = [word for word in words if word not in self.stopwords]

        
        return " ".join(filtered_words)
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """
        Preprocess multiple texts in batch.
        
        Args:
            texts: List of raw Vietnamese texts
            
        Returns:
            List[str]: List of preprocessed texts
        """
        return [self.preprocess(text) for text in texts]
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Vietnamese text into words.
        
        Args:
            text: Raw Vietnamese text
            
        Returns:
            List[str]: List of tokens
        """
        if not text or not text.strip():
            return []
        
        tokens = word_tokenize(text, format="text")
        return tokens.split()


def create_nlp_processor(stopwords: set[str]) -> NLPProcessor:
    """
    Factory function to create NLP processor instance.
    
    Args:
        stopwords: Set of Vietnamese stopwords
        
    Returns:
        NLPProcessor: Configured NLP processor
    """
    return NLPProcessor(stopwords)
