from typing import Any, Callable, List

_current_effects: List[Callable] = []

def use_effect(effect: Callable, dependencies: List[Any] = None):
    _current_effects.append(effect) 