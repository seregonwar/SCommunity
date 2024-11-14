from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from ..hooks import use_state, use_effect
from ..core import VirtualNode
from .state import State
from ..layout.grid import Grid
from ..layout.constraints import ConstraintManager, AdvancedConstraints

@dataclass
class DragState:
    is_dragging: bool = False
    start_pos: Optional[Tuple[int, int]] = None
    current_pos: Optional[Tuple[int, int]] = None
    offset: Optional[Tuple[int, int]] = None

class StateValue:
    def __init__(self, initial_value):
        self._state = State(initial_value)
        
    def get(self):
        return self._state.get()
        
    def set(self, value):
        self._state.set(value)

def use_draggable(widget_id: str, enabled: bool = True, constraints: Optional[AdvancedConstraints] = None):
    drag_state = StateValue(DragState())
    pos_x = StateValue(0)
    pos_y = StateValue(0)
    width = StateValue(100)
    height = StateValue(100)
    
    def handle_drag_start(event):
        if not enabled:
            return
        
        mouse_pos = (event.x, event.y)
        offset = (
            mouse_pos[0] - pos_x.get(),
            mouse_pos[1] - pos_y.get()
        )
        
        drag_state.set(DragState(
            is_dragging=True,
            start_pos=mouse_pos,
            current_pos=mouse_pos,
            offset=offset
        ))
    
    def handle_drag(event):
        current_state = drag_state.get()
        if not current_state.is_dragging:
            return
        
        new_x = event.x - current_state.offset[0]
        new_y = event.y - current_state.offset[1]
        
        if constraints and constraints.bounds:
            new_x = max(constraints.bounds.min_x, min(constraints.bounds.max_x, new_x))
            new_y = max(constraints.bounds.min_y, min(constraints.bounds.max_y, new_y))
        
        pos_x.set(new_x)
        pos_y.set(new_y)
    
    def handle_drag_end(event):
        drag_state.set(DragState())
    
    return {
        "position": (pos_x.get(), pos_y.get()),
        "size": (width.get(), height.get()),
        "is_dragging": drag_state.get().is_dragging,
        "handlers": {
            "onMouseDown": handle_drag_start,
            "onMouseMove": handle_drag,
            "onMouseUp": handle_drag_end
        }
    } 