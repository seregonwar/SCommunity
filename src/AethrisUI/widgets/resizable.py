from typing import Dict, Any, Tuple
from ..core import VirtualNode
from ..hooks import use_state

def ResizeHandle(props: Dict[str, Any]) -> VirtualNode:
    position = props.get("position", "se")  # ne, nw, se, sw
    
    style = {
        "position": "absolute",
        "width": "10px",
        "height": "10px",
        "background": "rgba(0,0,0,0.2)",
        "border-radius": "50%",
        "cursor": f"{position}-resize"
    }
    
    if "n" in position:
        style["top"] = "-5px"
    if "s" in position:
        style["bottom"] = "-5px"
    if "e" in position:
        style["right"] = "-5px"
    if "w" in position:
        style["left"] = "-5px"
    
    return VirtualNode(
        component_type="div",
        props={
            "style": style,
            "onMouseDown": props.get("onMouseDown")
        },
        children=[]
    )

def use_resizable(initial_size: Tuple[int, int] = (100, 100)):
    size, set_size = use_state(initial_size)
    is_resizing, set_is_resizing = use_state(False)
    resize_handle, set_resize_handle = use_state(None)
    
    def start_resize(handle: str, event):
        set_is_resizing(True)
        set_resize_handle(handle)
    
    def handle_resize(event):
        if not is_resizing:
            return
        
        # Implementa la logica di resize basata su resize_handle
        # e la posizione corrente del mouse
        
    def stop_resize():
        set_is_resizing(False)
        set_resize_handle(None)
    
    return {
        "size": size,
        "handlers": {
            "onMouseMove": handle_resize,
            "onMouseUp": stop_resize
        },
        "resize_handles": [
            ResizeHandle({"position": "ne", "onMouseDown": lambda e: start_resize("ne", e)}),
            ResizeHandle({"position": "nw", "onMouseDown": lambda e: start_resize("nw", e)}),
            ResizeHandle({"position": "se", "onMouseDown": lambda e: start_resize("se", e)}),
            ResizeHandle({"position": "sw", "onMouseDown": lambda e: start_resize("sw", e)})
        ]
    } 