from typing import Dict, List, Callable, Any

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def emit(self, event: str, *args: Any):
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args) 