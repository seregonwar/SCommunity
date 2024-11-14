from typing import Callable, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Request:
    method: str
    path: str
    headers: Dict[str, str]
    body: Any

@dataclass
class Response:
    status: int = 200
    headers: Dict[str, str] = None
    body: Any = None

class MiddlewareChain:
    def __init__(self):
        self.middlewares: List[Callable] = []
    
    def use(self, middleware: Callable):
        self.middlewares.append(middleware)
    
    async def handle(self, request: Request) -> Response:
        async def execute_middleware(index: int) -> Response:
            if index >= len(self.middlewares):
                return Response()
            
            return await self.middlewares[index](request, lambda: execute_middleware(index + 1))
        
        return await execute_middleware(0)

class APIRouter:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.middleware = MiddlewareChain()
    
    def route(self, path: str, methods: List[str] = ['GET']):
        def decorator(handler: Callable):
            for method in methods:
                if path not in self.routes:
                    self.routes[path] = {}
                self.routes[path][method] = handler
            return handler
        return decorator
    
    async def handle_request(self, request: Request) -> Response:
        # Prima esegui i middleware
        response = await self.middleware.handle(request)
        if response.status != 200:
            return response
        
        # Poi gestisci la route
        if request.path in self.routes and request.method in self.routes[request.path]:
            handler = self.routes[request.path][request.method]
            return await handler(request)
        
        return Response(status=404) 