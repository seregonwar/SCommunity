from typing import List, Callable, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Context:
    """Contesto per il middleware"""
    component: Any
    props: dict
    state: dict
    metadata: dict = None

class MiddlewareChain:
    def __init__(self):
        self._middleware: List[Callable] = []
        
    def use(self, middleware: Callable):
        """Aggiunge un middleware alla catena"""
        self._middleware.append(middleware)
        
    async def execute(self, context: Context) -> Context:
        """Esegue la catena di middleware"""
        current_context = context
        
        for middleware in self._middleware:
            try:
                current_context = await middleware(current_context)
            except Exception as e:
                logger.error(f"Middleware execution failed: {e}")
                raise
                
        return current_context 