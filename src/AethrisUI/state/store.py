from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from ..core.context import create_context

@dataclass
class Action:
    type: str
    payload: Any = None

class Store:
    def __init__(self, reducer: Callable[[Dict, Action], Dict], initial_state: Dict):
        self._state = initial_state
        self._reducer = reducer
        self._subscribers: List[Callable] = []
        self.context = create_context('store')
    
    def get_state(self) -> Dict:
        return self._state
    
    def dispatch(self, action: Action):
        self._state = self._reducer(self._state, action)
        for subscriber in self._subscribers:
            subscriber(self._state)
    
    def subscribe(self, callback: Callable):
        self._subscribers.append(callback)
        return lambda: self._subscribers.remove(callback)

def create_store(reducer: Callable[[Dict, Action], Dict], initial_state: Dict = None) -> Store:
    return Store(reducer, initial_state)

def use_selector(selector: Callable) -> Any:
    from ..hooks import use_context, use_state, use_effect
    
    store = use_context(Store.context)
    selected_state, set_selected_state = use_state(selector(store.get_state()))
    
    def handle_change(new_state: Dict):
        new_selected = selector(new_state)
        if new_selected != selected_state:
            set_selected_state(new_selected)
    
    use_effect(lambda: store.subscribe(handle_change), [])
    
    return selected_state