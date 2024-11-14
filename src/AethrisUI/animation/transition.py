from typing import Any, Callable
from dataclasses import dataclass
from .easing import Easing
import time

@dataclass
class Transition:
    property: str
    duration: int  # in milliseconds
    easing: str = "linear"
    delay: int = 0
    
    def __init__(self, property: str, duration: int, easing: str = "linear"):
        self.property = property
        self.duration = duration
        self.easing = easing
        self._start_value = None
        self._end_value = None
        self._start_time = None
    
    def start(self, start_value: Any, end_value: Any):
        self._start_value = start_value
        self._end_value = end_value
        self._start_time = time.time()
    
    def get_current_value(self) -> Any:
        if not self._start_time:
            return self._end_value
            
        progress = (time.time() - self._start_time) / (self.duration / 1000)
        if progress >= 1:
            return self._end_value
            
        eased_progress = Easing.get_easing_function(self.easing)(progress)
        return self._interpolate(self._start_value, self._end_value, eased_progress)
    
    def _interpolate(self, start: Any, end: Any, progress: float) -> Any:
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            return start + (end - start) * Easing.get_easing_function(self.easing)(progress)
        return end if progress > 0.5 else start 