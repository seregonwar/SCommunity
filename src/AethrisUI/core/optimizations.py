from typing import Dict, Any, Set
import hashlib

class StyleCache:
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def get_computed_style(cls, style: Dict[str, Any]) -> Dict[str, Any]:
        style_hash = cls._hash_style(style)
        if style_hash in cls._cache:
            return cls._cache[style_hash]
            
        computed = cls._compute_style(style)
        cls._cache[style_hash] = computed
        return computed
    
    @staticmethod
    def _hash_style(style: Dict[str, Any]) -> str:
        return hashlib.md5(str(sorted(style.items())).encode()).hexdigest()

class RenderOptimizer:
    def __init__(self):
        self._last_render: Dict[int, str] = {}
        self._dirty_components: Set[int] = set()
    
    def should_update(self, component_id: int, new_props: Dict[str, Any]) -> bool:
        props_hash = self._hash_props(new_props)
        should_update = props_hash != self._last_render.get(component_id)
        
        if should_update:
            self._last_render[component_id] = props_hash
            self._dirty_components.add(component_id)
            
        return should_update
    
    @staticmethod
    def _hash_props(props: Dict[str, Any]) -> str:
        return hashlib.md5(str(sorted(props.items())).encode()).hexdigest() 