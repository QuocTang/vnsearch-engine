"""Simple in-memory cache"""

import time
from typing import Optional, Any, Dict


class Cache:
    """Simple in-memory cache"""
    
    def __init__(self):
        self.store: Dict[str, tuple] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.store:
            return None
        
        value, expiry = self.store[key]
        if expiry and time.time() > expiry:
            del self.store[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional TTL"""
        expiry = time.time() + ttl if ttl else None
        self.store[key] = (value, expiry)
    
    def clear(self) -> None:
        """Clear all cache"""
        self.store.clear()
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self.store:
            del self.store[key]


# Global cache instance
cache = Cache()
