from typing import Dict, Any, Callable
import logging
from pathlib import Path
import asyncio
import weakref

logger = logging.getLogger(__name__)

class ResourceManager:
    def __init__(self):
        self._resources: Dict[str, Any] = {}
        self._cleanup_handlers: Dict[str, Callable] = {}
        self._refs = weakref.WeakValueDictionary()
        
    async def load(self, resource_id: str, loader: Callable):
        """Carica una risorsa in modo asincrono"""
        try:
            resource = await loader()
            self._resources[resource_id] = resource
            self._refs[resource_id] = resource
            return resource
        except Exception as e:
            logger.error(f"Failed to load resource {resource_id}: {e}")
            raise
            
    def register_cleanup(self, resource_id: str, cleanup: Callable):
        """Registra una funzione di cleanup per una risorsa"""
        self._cleanup_handlers[resource_id] = cleanup
        
    async def cleanup(self):
        """Pulisce tutte le risorse"""
        for resource_id, handler in self._cleanup_handlers.items():
            try:
                await handler(self._resources.get(resource_id))
            except Exception as e:
                logger.error(f"Cleanup failed for {resource_id}: {e}") 