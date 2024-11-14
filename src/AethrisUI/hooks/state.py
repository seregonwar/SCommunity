from typing import Any, Tuple, Callable
from ..core.state import State

def use_state(initial_value: Any) -> Tuple[State, Callable]:
    state = State(initial_value)
    return state, state.set 