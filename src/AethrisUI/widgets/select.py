from typing import Dict, Any, List, Union
from ..core import VirtualNode
from ..styling import Style
from ..theme import Theme
from .container import Container
from .text import Text

def Select(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un componente select.
    
    Args:
        props: {
            "options": List[Dict[str, str]],  # Lista di opzioni {value: str, label: str}
            "value": str,                     # Valore selezionato
            "onChange": Callable,             # Callback per il cambio di selezione
            "placeholder": str,               # Testo placeholder
            "disabled": bool,                 # Se disabilitato
            "style": Dict[str, Any]          # Stili aggiuntivi
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
        "cursor": "pointer",
        "position": "relative",
        "display": "flex",
        "align_items": "center",
        "justify_content": "space-between",
        **props.get("style", {})
    }
    
    if props.get("disabled"):
        base_style.update({
            "opacity": "0.5",
            "cursor": "not-allowed",
            "background": Theme.current.colors["background"]
        })
    
    # Trova l'opzione selezionata
    selected_option = None
    options = props.get("options", [])
    value = props.get("value")
    
    if value:
        for option in options:
            if option["value"] == value:
                selected_option = option
                break
    
    # Testo da mostrare
    display_text = ""
    if selected_option:
        display_text = selected_option["label"]
    elif props.get("placeholder"):
        display_text = props["placeholder"]
        base_style["color"] = Theme.current.colors["border"]
    
    # Icona dropdown
    arrow_style = {
        "width": "0",
        "height": "0",
        "border_left": "5px solid transparent",
        "border_right": "5px solid transparent",
        "border_top": f"5px solid {Theme.current.colors['text']}",
        "margin_left": "8px"
    }
    
    return Container({
        "children": [
            Text(display_text),
            Container({"style": arrow_style})  # Freccia dropdown
        ],
        "onClick": lambda: None if props.get("disabled") else None,  # Gestione click
        "style": base_style
    }) 