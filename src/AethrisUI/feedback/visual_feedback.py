from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from ..platform import Color

@dataclass
class FeedbackEffect:
    type: str  # "highlight", "shadow", "pulse", "shake"
    color: Optional[Color] = None
    duration: int = 300
    intensity: float = 1.0

class VisualFeedback:
    @staticmethod
    def create_drag_feedback(is_valid: bool = True) -> Dict[str, Any]:
        return {
            "opacity": "0.8",
            "transform": "scale(1.05)",
            "box-shadow": (
                "0 8px 16px rgba(0,128,0,0.2)" if is_valid
                else "0 8px 16px rgba(255,0,0,0.2)"
            )
        }
    
    @staticmethod
    def create_drop_preview(position: Tuple[int, int], size: Tuple[int, int]) -> Dict[str, Any]:
        return {
            "position": "absolute",
            "left": f"{position[0]}px",
            "top": f"{position[1]}px",
            "width": f"{size[0]}px",
            "height": f"{size[1]}px",
            "border": "2px dashed rgba(0,0,0,0.2)",
            "background": "rgba(0,0,0,0.05)",
            "pointer-events": "none"
        }
    
    @staticmethod
    def apply_effect(effect: FeedbackEffect) -> Dict[str, Any]:
        if effect.type == "highlight":
            return {
                "animation": {
                    "keyframes": [
                        {"opacity": 0, "time": 0},
                        {"opacity": effect.intensity, "time": 0.5},
                        {"opacity": 0, "time": 1}
                    ],
                    "duration": effect.duration,
                    "timing": "ease-out"
                },
                "background": effect.color.with_alpha(0.2).to_hex() if effect.color else None
            }
        elif effect.type == "shake":
            keyframes = {
                "0%": {"transform": "translateX(0)"},
                "25%": {"transform": f"translateX({4 * effect.intensity}px)"},
                "75%": {"transform": f"translateX(-{4 * effect.intensity}px)"},
                "100%": {"transform": "translateX(0)"}
            }
            return {
                "animation": f"shake {effect.duration}ms ease-in-out",
                "@keyframes shake": keyframes
            }
        elif effect.type == "pulse":
            color = effect.color or Color(0, 128, 255, 0.3)
            return {
                "animation": f"pulse {effect.duration}ms infinite",
                "@keyframes pulse": {
                    "0%": {"box-shadow": f"0 0 0 0 {color}"},
                    "70%": {"box-shadow": f"0 0 0 {10 * effect.intensity}px {color.with_alpha(0)}"},
                    "100%": {"box-shadow": f"0 0 0 0 {color.with_alpha(0)}"}
                }
            }
        elif effect.type == "shadow":
            return {
                "box-shadow": f"0 {4 * effect.intensity}px {8 * effect.intensity}px {effect.color or 'rgba(0,0,0,0.2)'}",
                "transition": f"box-shadow {effect.duration}ms ease-out"
            }
        
        return {}