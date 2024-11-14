from typing import Dict, Callable
from ..core import VirtualNode

class Router:
    def __init__(self):
        self.routes: Dict[str, Callable[[], VirtualNode]] = {}
        self.current_route = "/"
        
    def add_route(self, path: str, component: Callable[[], VirtualNode]):
        self.routes[path] = component
        
    def navigate(self, path: str):
        if path in self.routes:
            self.current_route = path
            # Trigger re-render