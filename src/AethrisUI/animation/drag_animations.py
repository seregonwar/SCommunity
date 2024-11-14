from typing import Dict, Any, Tuple
from ..core import VirtualNode
from .easing import Easing

class DragAnimations:
    @staticmethod
    def create_lift_animation(scale: float = 1.05, duration: int = 200) -> Dict[str, Any]:
        return {
            "transform": f"scale({scale})",
            "transition": f"transform {duration}ms {Easing.ease_out}",
            "box-shadow": "0 8px 16px rgba(0,0,0,0.2)",
            "z-index": 1000
        }
    
    @staticmethod
    def create_drop_animation(original_position: Tuple[int, int], duration: int = 300) -> Dict[str, Any]:
        return {
            "transform": "scale(1)",
            "transition": f"all {duration}ms {Easing.ease_out}",
            "left": f"{original_position[0]}px",
            "top": f"{original_position[1]}px"
        } 