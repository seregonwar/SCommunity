from typing import Dict, Any, Callable
from ..core import VirtualNode
from ..styling import Style
from ..theme import Theme
from .container import Container
from .text import Text

def Slider(props: Dict[str, Any]) -> VirtualNode:
    """
    Crea un componente slider.
    
    Args:
        props: {
            "min": float,             # Valore minimo
            "max": float,             # Valore massimo
            "value": float,           # Valore corrente
            "step": float,            # Incremento per step (opzionale)
            "onChange": Callable,     # Callback per il cambio di valore
            "disabled": bool,         # Se disabilitato
            "style": Dict[str, Any]   # Stili aggiuntivi
        }
    """
    base_style = {
        "width": "200px",
        "height": "4px",
        "background": Theme.current.colors["border"],
        "border_radius": "2px",
        "position": "relative",
        "cursor": "pointer" if not props.get("disabled") else "default",
        **props.get("style", {})
    }
    
    # Calcola la posizione del thumb
    min_val = float(props.get("min", 0))
    max_val = float(props.get("max", 100))
    current_val = float(props.get("value", min_val))
    
    # Normalizza il valore tra 0 e 1
    normalized = (current_val - min_val) / (max_val - min_val)
    
    # Stile della parte riempita
    filled_style = {
        "position": "absolute",
        "left": "0",
        "top": "0",
        "height": "100%",
        "width": f"{normalized * 100}%",
        "background": Theme.current.colors["primary"],
        "border_radius": "2px"
    }
    
    # Stile del thumb
    thumb_style = {
        "position": "absolute",
        "width": "16px",
        "height": "16px",
        "background": Theme.current.colors["primary"],
        "border_radius": "50%",
        "top": "-6px",
        "left": f"calc({normalized * 100}% - 8px)",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
    }
    
    if props.get("disabled"):
        base_style.update({
            "opacity": "0.5",
            "cursor": "not-allowed"
        })
    
    # Valore testuale
    value_text = Text(str(int(current_val)), style={
        "position": "absolute",
        "top": "-20px",
        "left": f"calc({normalized * 100}% - 10px)",
        "color": Theme.current.colors["text"]
    })
    
    return Container({
        "children": [
            Container({"style": filled_style}),  # Parte riempita
            Container({"style": thumb_style}),   # Thumb
            value_text                          # Valore
        ],
        "style": base_style
    }) 