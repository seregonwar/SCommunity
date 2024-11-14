from typing import Dict, Any, Callable, List
from ..core import VirtualNode
from ..styling import Style
from ..theme import Theme
from .container import Container
from .text import Text

def RadioButton(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un gruppo di radio button.
    
    Args:
        props: {
            "name": str,              # Nome del gruppo di radio button
            "options": List[str],     # Lista delle opzioni
            "value": str,             # Valore selezionato
            "onChange": Callable,     # Callback per il cambio di selezione
            "disabled": bool,         # Se disabilitato
            "style": Dict[str, Any]   # Stili aggiuntivi
        }
    """
    style = {
        "display": "flex",
        "flex_direction": "column",
        "gap": "8px",
        **props.get("style", {})
    }
    
    radio_style = {
        "width": "16px",
        "height": "16px",
        "border": f"2px solid {Theme.current.colors['border']}",
        "border_radius": "50%",
        "background": Theme.current.colors["surface"],
        "margin_right": "8px"
    }
    
    selected_radio_style = {
        **radio_style,
        "background": Theme.current.colors["primary"],
        "border_color": Theme.current.colors["primary"]
    }
    
    disabled_style = {
        "opacity": "0.5",
        "cursor": "default"
    }
    
    def create_radio_option(option: str):
        is_selected = option == props.get("value")
        is_disabled = props.get("disabled", False)
        
        option_style = {
            "display": "flex",
            "align_items": "center",
            "cursor": "pointer" if not is_disabled else "default",
            **(disabled_style if is_disabled else {})
        }
        
        return Container({
            "children": [
                Container({
                    "style": selected_radio_style if is_selected else radio_style
                }),
                Text(option, style={
                    "color": Theme.current.colors["text"],
                    "margin_left": "8px"
                })
            ],
            "onClick": (lambda o=option: props["onChange"](o)) 
                      if not is_disabled and "onChange" in props else None,
            "style": option_style
        })
    
    return Container({
        "children": [create_radio_option(opt) for opt in props.get("options", [])],
        "style": style
    }) 