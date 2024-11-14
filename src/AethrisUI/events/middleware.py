from typing import Callable, Any, List
from dataclasses import dataclass

@dataclass
class EventContext:
    type: str
    target: Any
    data: Any
    prevented: bool = False
    
    def prevent_default(self):
        self.prevented = True

class EventMiddleware:
    def __init__(self):
        self._middlewares: List[Callable] = []
        
    def use(self, middleware: Callable):
        self._middlewares.append(middleware)
        
    async def handle(self, context: EventContext):
        for middleware in self._middlewares:
            await middleware(context) 