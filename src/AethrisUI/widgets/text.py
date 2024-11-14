from typing import Union, Dict, Any
from ..core import VirtualNode
from ..platform.color import Color
from ..styling import Style
from ..theme import Theme

def Text(text: Union[str, int, float], color: Color = None, style: Dict[str, Any] = None) -> VirtualNode:
    """
    Crea un componente di testo.
    
    Args:
        text: Il testo da visualizzare (può essere una stringa, un numero intero o decimale)
        color: Il colore del testo (opzionale)
        style: Stili aggiuntivi (opzionale)
    """
    base_style = Style.text()
    
    if color:
        base_style["color"] = color
        
    if style:
        base_style.update(style)
    
    return VirtualNode(
        component_type="text",
        props={
            "text": str(text),
            **base_style
        },
        children=[]
    )