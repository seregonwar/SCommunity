from typing import Dict, Any, Callable
from ..core import VirtualNode
from ..styling import Style
from ..theme import Theme
from .container import Container
from .text import Text

def Switch(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un componente switch (toggle).
    
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
    
    # Stile del track (la barra di sfondo)
    track_style = {
        "width": "36px",
        "height": "20px",
        "background": Theme.current.colors["border"],
        "border_radius": "10px",
        "position": "relative",
        "margin_right": "8px",
        "transition": "background 0.2s"
    }
    
    # Stile del thumb (il cerchio che si muove)
    thumb_style = {
        "width": "16px",
        "height": "16px",
        "background": Theme.current.colors["surface"],
        "border_radius": "50%",
        "position": "absolute",
        "top": "2px",
        "left": "2px",
        "transition": "left 0.2s, background 0.2s",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
    }
    
    if props.get("checked"):
        track_style.update({
            "background": Theme.current.colors["primary"]
        })
        thumb_style.update({
            "left": "18px",
            "background": "#ffffff"
        })
    
    if props.get("disabled"):
        style.update({
            "opacity": "0.5",
            "cursor": "default"
        })
    
    return Container({
        "children": [
            Container({
                "children": [
                    Container({"style": thumb_style})
                ],
                "style": track_style
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