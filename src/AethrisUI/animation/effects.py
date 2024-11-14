from dataclasses import dataclass
from typing import Dict, Any, Optional
from ..platform.color import Color

@dataclass
class RippleEffect:
    x: int
    y: int
    size: int = 0
    opacity: float = 0.5
    duration: int = 600  # ms
    
    def update(self, progress: float):
        self.size = int(progress * 150)  # Dimensione massima del ripple
        self.opacity = 0.5 * (1 - progress)

@dataclass
class ElevationEffect:
    level: int
    color: Color
    
    def get_shadow(self) -> str:
        if self.level == 0:
            return "none"
        alpha = min(0.2 + (self.level * 0.02), 0.4)
        blur = self.level * 4
        spread = self.level * 2
        y_offset = self.level * 2
        return f"0 {y_offset}px {blur}px {spread}px rgba({self.color.r},{self.color.g},{self.color.b},{alpha})"

class ButtonEffects:
    @staticmethod
    def create_transition(property: str, duration: int = 200) -> str:
        return f"{property} {duration}ms cubic-bezier(0.4, 0, 0.2, 1)"
    
    @staticmethod
    def get_transitions() -> str:
        transitions = [
            "transform",
            "background-color",
            "box-shadow",
            "opacity"
        ]
        return ", ".join([ButtonEffects.create_transition(prop) for prop in transitions]) 