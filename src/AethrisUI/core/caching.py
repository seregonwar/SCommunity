from typing import Dict, Any, Optional
import time
import logging
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)

class RenderCache:
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._max_size = max_size
        self._ttl = ttl
        
    def get(self, key: str) -> Optional[Any]:
        """Ottiene un elemento dalla cache"""
        if key in self._cache:
            if time.time() - self._timestamps[key] > self._ttl:
                self._remove(key)
                return None
            return self._cache[key]
        return None
        
    def set(self, key: str, value: Any):
        """Imposta un elemento nella cache"""
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
            
        self._cache[key] = value
        self._timestamps[key] = time.time()
        
    def _remove(self, key: str):
        """Rimuove un elemento dalla cache"""
        del self._cache[key]
        del self._timestamps[key]
        
    def _evict_oldest(self):
        """Rimuove l'elemento più vecchio dalla cache"""
        oldest_key = min(self._timestamps.items(), key=lambda x: x[1])[0]
        self._remove(oldest_key) 