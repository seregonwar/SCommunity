from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
from .easing import Easing
import time

@dataclass
class KeyFrame:
    properties: Dict[str, Any]
    time: float
    easing: Callable[[float], float] = Easing.linear

class Animation:
    def __init__(self):
        self.keyframes: List[KeyFrame] = []
        self._current_frame = 0
        self._start_time = 0
        self._is_running = False
        self._on_update: Optional[Callable[[Dict[str, Any]], None]] = None
    
    def add_keyframe(self, properties: Dict[str, Any], time: float, easing: Callable = None):
        if easing is None:
            easing = Easing.linear
        self.keyframes.append(KeyFrame(properties, time, easing))
        self.keyframes.sort(key=lambda k: k.time)
    
    def start(self, on_update: Callable[[Dict[str, Any]], None]):
        self._on_update = on_update
        self._start_time = time.time()
        self._current_frame = 0
        self._is_running = True
        self._update()
    
    def _update(self):
        if not self._is_running:
            return
        
        current_time = time.time() - self._start_time
        current_frame = self.keyframes[self._current_frame]
        next_frame = self.keyframes[self._current_frame + 1] if self._current_frame + 1 < len(self.keyframes) else None
        
        if next_frame and current_time >= next_frame.time:
            self._current_frame += 1
            if self._current_frame >= len(self.keyframes) - 1:
                self._is_running = False
                if self._on_update:
                    self._on_update(self.keyframes[-1].properties)
                return
        
        if next_frame:
            progress = (current_time - current_frame.time) / (next_frame.time - current_frame.time)
            progress = min(1.0, max(0.0, progress))
            eased_progress = next_frame.easing(progress)
            
            interpolated = self._interpolate(
                current_frame.properties,
                next_frame.properties,
                eased_progress
            )
            
            if self._on_update:
                self._on_update(interpolated)
    
    def _interpolate(self, start: Dict[str, Any], end: Dict[str, Any], progress: float) -> Dict[str, Any]:
        result = {}
        for key in end:
            if key in start:
                if isinstance(start[key], (int, float)):
                    result[key] = start[key] + (end[key] - start[key]) * progress
                else:
                    result[key] = end[key] if progress > 0.5 else start[key]
            else:
                result[key] = end[key]
        return result 