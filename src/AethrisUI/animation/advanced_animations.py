from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
import math
import time

@dataclass
class AnimationKeyframe:
    properties: Dict[str, Any]
    time: float  # 0.0 to 1.0
    easing: Callable[[float], float]

@dataclass
class AnimationState:
    value: Any
    velocity: float = 0
    target: Any = None

class AdvancedAnimation:
    def __init__(self):
        self.keyframes: List[AnimationKeyframe] = []
        self.duration: int = 1000  # ms
        self.repeat: bool = False
        self.reverse: bool = False
        self.on_complete: Optional[Callable] = None
    
    def add_keyframe(self, properties: Dict[str, Any], time: float, easing: Callable = None):
        if easing is None:
            easing = lambda x: x  # Linear
        self.keyframes.append(AnimationKeyframe(properties, time, easing))
        self.keyframes.sort(key=lambda k: k.time)
    
    def interpolate(self, progress: float) -> Dict[str, Any]:
        if not self.keyframes:
            return {}
        
        # Trova i keyframe prima e dopo il progress attuale
        next_idx = 0
        while next_idx < len(self.keyframes) and self.keyframes[next_idx].time < progress:
            next_idx += 1
        
        if next_idx == 0:
            return self.keyframes[0].properties
        if next_idx == len(self.keyframes):
            return self.keyframes[-1].properties
        
        prev = self.keyframes[next_idx - 1]
        next = self.keyframes[next_idx]
        
        # Calcola il progress tra i due keyframe
        frame_progress = (progress - prev.time) / (next.time - prev.time)
        eased_progress = next.easing(frame_progress)
        
        # Interpola le proprietà
        result = {}
        for key in prev.properties:
            if key in next.properties:
                start_val = prev.properties[key]
                end_val = next.properties[key]
                if isinstance(start_val, (int, float)):
                    result[key] = start_val + (end_val - start_val) * eased_progress
                else:
                    result[key] = end_val if eased_progress > 0.5 else start_val
        
        return result 

class SpringAnimation:
    def __init__(self, tension: float = 170, friction: float = 26):
        self.tension = tension
        self.friction = friction
        self.states: Dict[str, AnimationState] = {}
    
    def animate(self, property: str, target: Any):
        # Implementare animazioni spring physics
        pass