from typing import Any, Callable, List

class State:
    def __init__(self, initial_value):
        self._value = initial_value
        
    def get(self):
        return self._value
        
    def set(self, new_value):
        self._value = new_value 