from typing import Optional, Callable, List
from ..core import VirtualNode
from ..hooks import use_state

class ErrorBoundary:
    def __init__(self, fallback: Callable[[Exception], VirtualNode]):
        self.fallback = fallback
        self.error: Optional[Exception] = None
    
    def catch(self, error: Exception):
        self.error = error
    
    def render(self, children: List[VirtualNode]) -> VirtualNode:
        if self.error:
            return self.fallback(self.error)
        
        try:
            return VirtualNode(
                component_type="error-boundary",
                props={},
                children=children
            )
        except Exception as e:
            self.catch(e)
            return self.fallback(e)

def use_error_boundary(fallback: Callable[[Exception], VirtualNode]):
    error, set_error = use_state(None)
    
    def error_handler(e: Exception):
        set_error(e)
        return fallback(e)
    
    return error_handler 