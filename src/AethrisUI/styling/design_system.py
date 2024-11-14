from typing import Dict, Any, List
from ..theme import Theme
from .units import Px

class BorderRadius:
    @staticmethod
    def all(value: Px) -> str:
        return str(value)
    
    @staticmethod
    def top(value: Px) -> str:
        return f"{value} {value} 0 0"
    
    @staticmethod
    def bottom(value: Px) -> str:
        return f"0 0 {value} {value}"
    
    @staticmethod
    def left(value: Px) -> str:
        return f"{value} 0 0 {value}"
    
    @staticmethod
    def right(value: Px) -> str:
        return f"0 {value} {value} 0"
    
    @staticmethod
    def custom(top_left: Px, top_right: Px, bottom_right: Px, bottom_left: Px) -> str:
        return f"{top_left} {top_right} {bottom_right} {bottom_left}"

class Shadow:
    def __init__(self, x: Px, y: Px, blur: Px, spread: Px, color: str):
        self.x = x
        self.y = y
        self.blur = blur
        self.spread = spread
        self.color = color
    
    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.blur} {self.spread} {self.color}"

class DesignSystem:
    @staticmethod
    def elevation(level: int) -> Dict[str, Any]:
        shadows = {
            0: [],
            1: [Shadow(Px(0), Px(2), Px(4), Px(0), "rgba(0,0,0,0.1)")],
            2: [
                Shadow(Px(0), Px(4), Px(8), Px(0), "rgba(0,0,0,0.1)"),
                Shadow(Px(0), Px(2), Px(4), Px(0), "rgba(0,0,0,0.05)")
            ],
            3: [
                Shadow(Px(0), Px(8), Px(16), Px(0), "rgba(0,0,0,0.1)"),
                Shadow(Px(0), Px(4), Px(8), Px(0), "rgba(0,0,0,0.05)")
            ]
        }
        return {"box_shadow": " ,".join(str(s) for s in shadows.get(level, []))}
    
    @staticmethod
    def glass_effect(opacity: float = 0.1) -> Dict[str, Any]:
        return {
            "background": f"rgba(255,255,255,{opacity})",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(255,255,255,0.2)"
        }
    
    @staticmethod
    def neumorphism(light: bool = True) -> Dict[str, Any]:
        if light:
            return {
                "background": "#e0e0e0",
                "box_shadow": f"{Shadow(Px(-8), Px(-8), Px(15), Px(0), '#ffffff')}, "
                            f"{Shadow(Px(8), Px(8), Px(15), Px(0), 'rgba(0,0,0,0.1)')}"
            }
        return {
            "background": "#2d2d2d",
            "box_shadow": f"{Shadow(Px(-8), Px(-8), Px(15), Px(0), '#3d3d3d')}, "
                        f"{Shadow(Px(8), Px(8), Px(15), Px(0), '#1d1d1d')}"
        }

class ModernStyle:
    @staticmethod
    def button(variant: str = "default") -> dict:
        theme = Theme.get_current()  # Usa il tema globale invece di crearne uno nuovo
        base_style = {
            "background": theme.colors["primary"],
            "color": theme.colors["text"],
            "padding": "10px 20px",
            "border_radius": "4px", 
            "border": f"1px solid {theme.colors['border']}",
            "cursor": "pointer",
            "transition": "all 0.2s ease-in-out"
        }
        
        variants = {
            "filled": {
                "background": theme.colors["primary"],
                "color": "#ffffff"
            },
            "outlined": {
                "background": "transparent",
                "border": f"2px solid {theme.colors['primary']}",
                "color": theme.colors["primary"]
            },
            "text": {
                "background": "transparent",
                "border": "none",
                "color": theme.colors["primary"]
            }
        }
        
        if variant in variants:
            base_style.update(variants[variant])
            
        return base_style
    
    @staticmethod
    def glass_effect(opacity: float = 0.1) -> Dict[str, Any]:
        return {
            "background": f"rgba(255,255,255,{opacity})",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(255,255,255,0.2)"
        }
    
    @staticmethod
    def gradient(stops: List[Dict[str, Any]], angle: int = 0) -> Dict[str, str]:
        stops_str = ", ".join([f"{stop['color']} {stop['position'] * 100}%" for stop in stops])
        return {
            "background": f"linear-gradient({angle}deg, {stops_str})"
        }
    
    @staticmethod
    def card(variant: str = "elevated") -> Dict[str, Any]:
        base = {
            "padding": Px(24),
            "border_radius": BorderRadius.all(Px(16)),
            "background": ModernStyle._theme.surface
        }
        
        variants = {
            "elevated": {
                **base,
                **DesignSystem.elevation(2)
            },
            "glass": {
                **base,
                **DesignSystem.glass_effect()
            },
            "neumorphic": {
                **base,
                **DesignSystem.neumorphism()
            }
        }
        
        return variants.get(variant, variants["elevated"]) 