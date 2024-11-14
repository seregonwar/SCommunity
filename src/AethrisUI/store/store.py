from typing import Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class Action:
    type: str
    payload: Any = None

class Store:
    def __init__(self, reducer: Callable, initial_state: Dict[str, Any]):
        self._state = initial_state
        self._reducer = reducer
        self._subscribers = []
    
    def dispatch(self, action: Action):
        self._state = self._reducer(self._state, action)
        self._notify_subscribers()
    
    def subscribe(self, callback: Callable):
        self._subscribers.append(callback)
        return lambda: self._subscribers.remove(callback) 