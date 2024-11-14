from typing import Dict, Any, Callable
from ..core import VirtualNode
from ..styling import Style
from ..theme import Theme
from .container import Container
from .text import Text

def Input(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un componente input.
    
    Args:
        props: {
            "type": str,              # "text", "password", "number", etc.
            "placeholder": str,       # Testo placeholder
            "value": str,             # Valore corrente
            "onChange": Callable,     # Callback per il cambio di valore
            "disabled": bool,         # Se disabilitato
            "style": Dict[str, Any]   # Stili aggiuntivi
        }
    """
    base_style = {
        "padding": "8px 12px",
        "border": f"1px solid {Theme.current.colors['border']}",
        "border_radius": "4px",
        "background": Theme.current.colors["surface"],
        "color": Theme.current.colors["text"],
        "font_family": Theme.current.fonts["primary"],
        "font_size": "14px",
        "width": "200px",
        "outline": "none"
    }
    
    if props.get("disabled"):
        base_style.update({
            "opacity": "0.5",
            "cursor": "not-allowed",
            "background": Theme.current.colors["background"]
        })
    
    style = {
        **base_style,
        **props.get("style", {})
    }
    
    # Se è un input di tipo password, mostra pallini invece del testo
    display_value = ""
    if props.get("type") == "password" and props.get("value"):
        display_value = "•" * len(props["value"])
    else:
        display_value = props.get("value", "")
    
    # Se non c'è valore ma c'è placeholder, mostralo in grigio
    if not display_value and props.get("placeholder"):
        return Container({
            "children": [
                Text(props["placeholder"], style={
                    "color": Theme.current.colors["border"],
                    "position": "absolute",
                    "pointer_events": "none"
                })
            ],
            "style": style
        })
    
    return Container({
        "children": [
            Text(display_value)
        ],
        "onClick": lambda: None if props.get("disabled") else None,  # Gestione click
        "style": style
    }) 