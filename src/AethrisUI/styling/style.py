from typing import Dict, Any
from .units import Px

class Style:
    @staticmethod
    def merge(*styles: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for style in styles:
            result.update(style)
        return result
    
    @staticmethod
    def button() -> Dict[str, Any]:
        from ..theme import Theme
        theme = Theme.get_current()
        return {
            "background": theme.colors["primary"],
            "padding": Px(10),
            "border_radius": Px(5),
            "color": theme.colors["text"],
            "border": f"1px solid {theme.colors['border']}",
            "cursor": "pointer"
        }
    
    @staticmethod
    def container() -> Dict[str, Any]:
        from ..theme import Theme
        theme = Theme.get_current()
        return {
            "display": "flex",
            "flex_direction": "column",
            "background": theme.colors["background"],
            "padding": Px(10),
            "margin": Px(0)
        }
    
    @staticmethod
    def input() -> Dict[str, Any]:
        from ..theme import Theme
        theme = Theme.get_current()
        return {
            "padding": Px(8),
            "border": f"1px solid {theme.colors['border']}",
            "border_radius": Px(4),
            "background": theme.colors["surface"]
        }
    
    @staticmethod
    def text() -> Dict[str, Any]:
        from ..theme import Theme
        theme = Theme.get_current()
        return {
            "font_family": theme.fonts["primary"],
            "font_size": Px(14),
            "color": theme.colors["text"],
            "margin": Px(0)
        }