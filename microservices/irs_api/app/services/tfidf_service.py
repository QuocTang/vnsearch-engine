"""
TF-IDF vectorization service.
Handles training, saving, loading and transforming TF-IDF models.
"""

import joblib
from pathlib import Path
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class TFIDFService:
    """
    TF-IDF vectorization service for text to vector transformation.
    """
    
    def __init__(self):
        """Initialize TF-IDF service."""
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.is_fitted = False
    
    def train(
        self, 
        texts: List[str],
        max_features: int = 5000,
        min_df: int = 2,
        max_df: float = 0.8
    ) -> None:
        """
        Train TF-IDF model on corpus.
        
        Args:
            texts: List of preprocessed texts
            max_features: Maximum number of features
            min_df: Minimum document frequency
            max_df: Maximum document frequency (ratio)
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            lowercase=False,  # Already lowercased in preprocessing
tokenizer=lambda x: x.split()  # Already tokenized
        )
        
        self.vectorizer.fit(texts)
        self.is_fitted = True
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform texts to TF-IDF vectors.
        
        Args:
            texts: List of preprocessed texts
            
        Returns:
            np.ndarray: TF-IDF vectors (dense array)
            
        Raises:
            ValueError: If model not fitted
        """
        if not self.is_fitted or self.vectorizer is None:
            raise ValueError("TF-IDF model not fitted. Call train() or load() first.")
        
        # Transform and convert sparse matrix to dense array
        vectors = self.vectorizer.transform(texts).toarray()
        return vectors
    
    def save(self, model_path: str) -> None:
        """
        Save TF-IDF model to file.
        
        Args:
            model_path: Path to save model (*.pkl)
            
        Raises:
            ValueError: If model not fitted
        """
        if not self.is_fitted or self.vectorizer is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create parent directory if not exists
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save using joblib
        joblib.dump(self.vectorizer, model_path)
    
    def load(self, model_path: str) -> None:
        """
        Load TF-IDF model from file.
        
        Args:
            model_path: Path to model file
            
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.vectorizer = joblib.load(model_path)
        self.is_fitted = True
    
    def get_feature_names(self) -> List[str]:
        """
        Get vocabulary feature names.
        
        Returns:
            List[str]: List of feature names
            
        Raises:
            ValueError: If model not fitted
        """
        if not self.is_fitted or self.vectorizer is None:
            raise ValueError("Model not fitted")
        
        return self.vectorizer.get_feature_names_out().tolist()
    
    def get_vector_dimension(self) -> int:
        """
        Get dimension of TF-IDF vectors.
        
        Returns:
            int: Vector dimension
            
        Raises:
            ValueError: If model not fitted
        """
        if not self.is_fitted or self.vectorizer is None:
            raise ValueError("Model not fitted")
        
        return len(self.vectorizer.get_feature_names_out())
