from typing import Dict, Any, Callable
from ..core import VirtualNode
from ..styling import Style
from ..platform.color import Color
from ..theme import Theme
from .container import Container
from .text import Text

def Checkbox(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un componente checkbox.
    
    Args:
        props: {
            "label": str,              # Testo della label
            "checked": bool,           # Stato iniziale
            "onChange": Callable,      # Callback per il cambio di stato
            "disabled": bool,          # Se disabilitato
            "style": Dict[str, Any]    # Stili aggiuntivi
        }
    """
    style = {
        "display": "flex",
        "align_items": "center",
        "padding": "5px",
        "cursor": "pointer" if not props.get("disabled") else "default",
        **props.get("style", {})
    }
    
    checkbox_style = {
        "width": "16px",
        "height": "16px",
        "border": f"2px solid {Theme.current.colors['border']}",
        "background": Theme.current.colors["surface"],
        "margin_right": "8px",
        "border_radius": "3px"
    }
    
    if props.get("checked"):
        checkbox_style.update({
            "background": Theme.current.colors["primary"],
            "border_color": Theme.current.colors["primary"]
        })
    
    if props.get("disabled"):
        checkbox_style.update({
            "opacity": "0.5",
            "cursor": "default"
        })
    
    return Container({
        "children": [
            Container({
                "style": checkbox_style
            }),
            Text(props.get("label", ""), style={
                "color": Theme.current.colors["text"],
                "opacity": "0.5" if props.get("disabled") else "1"
            })
        ],
        "onClick": (lambda: props["onChange"](not props["checked"])) 
                   if not props.get("disabled") and "onChange" in props else None,
        "style": style
    }) 