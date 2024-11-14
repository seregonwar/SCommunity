from typing import Any, Callable, List
from .state import use_state
from .effect import use_effect

def use_memo(compute: Callable, dependencies: List[Any]) -> Any:
    state, set_state = use_state(None)
    
    def check_and_update():
        result = compute()
        if result != state.get():
            set_state(result)
    
    use_effect(check_and_update, dependencies)
    return state.get() 