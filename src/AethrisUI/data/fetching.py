from typing import Any, Callable, Dict, Optional
from functools import wraps
import asyncio
import time

class Cache:
    _cache: Dict[str, Any] = {}
    _timestamps: Dict[str, float] = {}
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: Optional[int] = None):
        cls._cache[key] = value
        cls._timestamps[key] = time.time() + (ttl or float('inf'))
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        if key in cls._cache and time.time() < cls._timestamps[key]:
            return cls._cache[key]
        return None

def use_query(key: str, fetch_fn: Callable, options: Dict[str, Any] = None):
    from ..hooks import use_state, use_effect
    
    data, set_data = use_state(None)
    loading, set_loading = use_state(True)
    error, set_error = use_state(None)
    
    async def fetch_data():
        try:
            cached = Cache.get(key)
            if cached:
                set_data(cached)
                set_loading(False)
                return
            
            result = await fetch_fn()
            Cache.set(key, result, options.get('ttl'))
            set_data(result)
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)
    
    use_effect(lambda: asyncio.create_task(fetch_data()), [key])
    
    return data, loading, error 