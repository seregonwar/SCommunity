from typing import Dict, Any
from ..core import VirtualNode
from ..core.draggable import use_draggable
from ..styling import Style
from .container import Container

def DraggableContainer(props: Dict[str, Any]) -> VirtualNode:
    draggable = use_draggable(
        widget_id=props.get("id", str(id(props))),
        enabled=props.get("draggable", True),
        constraints=props.get("constraints")
    )
    
    style = {
        **Style.container(),
        "position": "absolute",
        "left": f"{draggable['position'][0]}px",
        "top": f"{draggable['position'][1]}px",
        "width": f"{draggable['size'][0]}px",
        "height": f"{draggable['size'][1]}px",
        "cursor": "move" if props.get("draggable", True) else "default",
        "user-select": "none",
        **props.get("style", {})
    }
    
    if draggable["is_dragging"]:
        style.update({
            "opacity": "0.8",
            "box-shadow": "0 8px 16px rgba(0,0,0,0.2)",
            "z-index": "1000",
            "transform": "scale(1.02)"
        })
    
    return Container({
        **props,
        **draggable["handlers"],
        "style": style
    }) 