from typing import Dict, Any, Union, List
from dataclasses import dataclass
from .units import Px, Rem
from .theme import Theme
from .design_system import BorderRadius, Shadow

@dataclass
class GradientStop:
    color: str
    position: float  # 0.0 to 1.0

class ModernEffects:
    @staticmethod
    def gradient(stops: List[GradientStop], angle: int = 0) -> Dict[str, str]:
        stops_str = ", ".join([f"{stop.color} {stop.position * 100}%" for stop in stops])
        return {
            "background": f"linear-gradient({angle}deg, {stops_str})"
        }
    
    @staticmethod
    def glass(opacity: float = 0.1, blur: int = 10, border_opacity: float = 0.2) -> Dict[str, Any]:
        return {
            "background": f"rgba(255, 255, 255, {opacity})",
            "backdrop_filter": f"blur({blur}px)",
            "border": f"1px solid rgba(255, 255, 255, {border_opacity})",
            "-webkit-backdrop-filter": f"blur({blur}px)",
            "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "transition": "all 0.3s ease"
        }
    
    @staticmethod
    def glow(color: str, intensity: int = 20) -> Dict[str, Any]:
        return {
            "box_shadow": f"0 0 {intensity}px {color}",
            "transition": "box-shadow 0.3s ease"
        }
    
    @staticmethod
    def soft_shadow() -> Dict[str, Any]:
        return {
            "box_shadow": (
                "0 1px 1px rgba(0,0,0,0.08), "
                "0 2px 2px rgba(0,0,0,0.08), "
                "0 4px 4px rgba(0,0,0,0.08), "
                "0 8px 8px rgba(0,0,0,0.08)"
            )
        }
    
    @staticmethod
    def floating(level: int = 1) -> Dict[str, Any]:
        shadows = {
            1: "0 4px 8px rgba(0,0,0,0.08)",
            2: "0 8px 16px rgba(0,0,0,0.12)",
            3: "0 16px 32px rgba(0,0,0,0.16)"
        }
        return {
            "box_shadow": shadows.get(level, shadows[1]),
            "transform": "translateY(0)",
            "transition": "all 0.3s ease",
            ":hover": {
                "transform": "translateY(-4px)",
                "box_shadow": shadows.get(level + 1, shadows[3])
            }
        }
    
    @staticmethod
    def pulse(color: str) -> Dict[str, Any]:
        return {
            "animation": "pulse 2s infinite",
            "@keyframes pulse": {
                "0%": {
                    "box_shadow": f"0 0 0 0 {color}4D"  # 30% opacity
                },
                "70%": {
                    "box_shadow": f"0 0 0 10px {color}00"  # 0% opacity
                },
                "100%": {
                    "box_shadow": f"0 0 0 0 {color}00"
                }
            }
        }
    
    @staticmethod
    def noise(opacity: float = 0.05) -> Dict[str, Any]:
        return {
            "position": "relative",
            "overflow": "hidden",
            ":after": {
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": f"url('data:image/png;base64,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')",
                "opacity": str(opacity)
            }
        }

# Aggiorniamo ModernStyle per usare i nuovi effetti
class ModernStyle:
    @staticmethod
    def button(variant: str = "filled", effect: str = None) -> Dict[str, Any]:
        base = {
            "padding": f"{Px(12)} {Px(24)}",
            "border_radius": BorderRadius.all(Px(8)),
            "font_size": Rem(1),
            "font_weight": "500",
            "transition": "all 0.2s ease-in-out",
            "cursor": "pointer",
            "outline": "none",
            "border": "none",
            "position": "relative",
            "overflow": "hidden"
        }
        
        variants = {
            "filled": {
                **base,
                "background": Theme.current.primary,
                "color": "#ffffff",
                **ModernEffects.floating(1)
            },
            "outlined": {
                **base,
                "background": "transparent",
                "color": Theme.current.primary,
                "border": f"2px solid {Theme.current.primary}"
            },
            "glass": {
                **base,
                **ModernEffects.glass(),
                "color": Theme.current.text
            },
            "gradient": {
                **base,
                **ModernEffects.gradient([
                    GradientStop(Theme.current.primary, 0),
                    GradientStop(Theme.current.secondary, 1)
                ]),
                "color": "#ffffff"
            }
        }
        
        style = variants.get(variant, variants["filled"])
        
        if effect == "glow":
            style.update(ModernEffects.glow(Theme.current.primary))
        elif effect == "pulse":
            style.update(ModernEffects.pulse(Theme.current.primary))
        elif effect == "noise":
            style.update(ModernEffects.noise())
        
        return style 