"""
Stopwords loader utility for Vietnamese text processing.
Loads and caches Vietnamese stopwords from text file.
"""

from pathlib import Path
from functools import lru_cache
from typing import Set


@lru_cache(maxsize=1)
def load_stopwords(stopwords_path: str = "assets/txt/vietnamese-stopwords.txt") -> Set[str]:
    """
    Load Vietnamese stopwords from text file and cache in memory.
    
    Args:
        stopwords_path: Path to stopwords file (one word per line)
        
    Returns:
        Set[str]: Set of Vietnamese stopwords
        
    Raises:
        FileNotFoundError: If stopwords file doesn't exist
    """
    path = Path(stopwords_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Stopwords file not found: {stopwords_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace, filter empty lines
        stopwords = {line.strip() for line in f if line.strip()}
    
    return stopwords


def is_stopword(word: str, stopwords: Set[str]) -> bool:
    """
    Check if a word is a stopword.
    
    Args:
        word: Word to check
        stopwords: Set of stopwords
        
    Returns:
        bool: True if word is a stopword
    """
    return word.lower() in stopwords
