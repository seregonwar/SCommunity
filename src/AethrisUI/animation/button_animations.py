from dataclasses import dataclass
from typing import Dict, Any
from ..platform.color import Color

@dataclass
class ButtonState:
    idle: Dict[str, Any]
    hover: Dict[str, Any]
    active: Dict[str, Any]
    disabled: Dict[str, Any]

class ButtonAnimations:
    @staticmethod
    def create_state(base_color: Color) -> ButtonState:
        return ButtonState(
            idle={
                "background": base_color.to_hex(),
                "transform": "scale(1)",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
                "transition": "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
            },
            hover={
                "background": base_color.lighten(0.1).to_hex(),
                "transform": "scale(1.02) translateY(-1px)",
                "box_shadow": "0 4px 8px rgba(0,0,0,0.15)",
                "transition": "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
            },
            active={
                "background": base_color.darken(0.1).to_hex(),
                "transform": "scale(0.98) translateY(1px)",
                "box_shadow": "0 1px 2px rgba(0,0,0,0.2)",
                "transition": "all 50ms cubic-bezier(0.4, 0, 0.2, 1)"
            },
            disabled={
                "background": base_color.with_alpha(0.5).to_hex(),
                "transform": "scale(1)",
                "box_shadow": "none",
                "cursor": "not-allowed"
            }
        ) 