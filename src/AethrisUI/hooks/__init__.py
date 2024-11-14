from typing import Any, Callable, List
from ..core.state import State

def use_state(initial_value: Any):
    state = State(initial_value)
    return state.get, state.set

def use_effect(effect: Callable, dependencies: List[Any] = None):
    # Track previous dependencies
    prev_deps = getattr(use_effect, '_prev_deps', None)
    
    # Check if dependencies changed
    deps_changed = (
        dependencies is None or 
        prev_deps is None or
        len(dependencies) != len(prev_deps) or
        any(a != b for a, b in zip(dependencies, prev_deps))
    )
    
    if deps_changed:
        # Store new dependencies
        use_effect._prev_deps = dependencies
        # Execute effect
        return effect()

def use_memo(compute: Callable, dependencies: List[Any] = None):
    # Track previous value and dependencies 
    prev_value = getattr(use_memo, '_prev_value', None)
    prev_deps = getattr(use_memo, '_prev_deps', None)
    
    # Check if dependencies changed
    deps_changed = (
        dependencies is None or
        prev_deps is None or 
        len(dependencies) != len(prev_deps) or
        any(a != b for a, b in zip(dependencies, prev_deps))
    )
    
    if deps_changed:
        # Compute and store new value
        value = compute()
        use_memo._prev_value = value
        use_memo._prev_deps = dependencies
        return value
        
    return prev_value

def use_callback(callback: Callable, dependencies: List[Any] = None):
    def memoized_callback(*args, **kwargs):
        return callback(*args, **kwargs)
    
    return use_memo(
        lambda: memoized_callback,
        dependencies
    )

__all__ = ['use_state', 'use_effect', 'use_memo', 'use_callback']