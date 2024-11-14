from typing import Dict, Any
import hashlib

class OptimizedRenderer:
    def __init__(self):
        self._cache = {}
        
    def should_update(self, old_props: Dict[str, Any], new_props: Dict[str, Any]) -> bool:
        old_hash = self._hash_props(old_props)
        new_hash = self._hash_props(new_props)
        return old_hash != new_hash 