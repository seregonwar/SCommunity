from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class Anchor:
    target_id: str
    edge: str  # "left", "right", "top", "bottom", "center"
    offset: int = 0

@dataclass
class Bounds:
    min_x: int
    min_y: int
    max_x: int
    max_y: int

@dataclass
class AdvancedConstraints:
    anchors: Dict[str, Anchor] = field(default_factory=dict)  # edge -> anchor
    min_distance: Dict[str, int] = field(default_factory=dict)  # widget_id -> distance
    max_distance: Dict[str, int] = field(default_factory=dict)
    alignment: Optional[str] = None  # "start", "center", "end"
    distribution: Optional[str] = None  # "space-between", "space-around"
    flex: float = 1.0
    aspect_ratio: Optional[float] = None
    snap_to_grid: bool = False
    prevent_collision: bool = True
    bounds: Optional[Bounds] = None
    min_size: Optional[Tuple[int, int]] = None
    max_size: Optional[Tuple[int, int]] = None

class ConstraintManager:
    def __init__(self):
        self.widget_constraints: Dict[str, AdvancedConstraints] = {}
        self.widget_bounds: Dict[str, Tuple[int, int, int, int]] = {}  # x, y, width, height
    
    def add_widget(self, widget_id: str, constraints: AdvancedConstraints):
        self.widget_constraints[widget_id] = constraints
    
    def update_bounds(self, widget_id: str, bounds: Tuple[int, int, int, int]):
        self.widget_bounds[widget_id] = bounds
    
    def check_collision(self, widget_id: str, new_bounds: Tuple[int, int, int, int]) -> bool:
        for other_id, other_bounds in self.widget_bounds.items():
            if other_id != widget_id:
                if self._bounds_intersect(new_bounds, other_bounds):
                    return True
        return False
    
    def _bounds_intersect(self, a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> bool:
        return not (a[0] + a[2] < b[0] or
                   a[0] > b[0] + b[2] or
                   a[1] + a[3] < b[1] or
                   a[1] > b[1] + b[3])
    
    def apply_constraints(self, widget_id: str, position: Tuple[int, int], size: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        if widget_id not in self.widget_constraints:
            return position, size
        
        constraints = self.widget_constraints[widget_id]
        new_pos = list(position)
        new_size = list(size)
        
        # Applica vincoli di dimensione
        if constraints.min_size:
            new_size[0] = max(new_size[0], constraints.min_size[0])
            new_size[1] = max(new_size[1], constraints.min_size[1])
        if constraints.max_size:
            new_size[0] = min(new_size[0], constraints.max_size[0])
            new_size[1] = min(new_size[1], constraints.max_size[1])
        
        # Applica aspect ratio
        if constraints.aspect_ratio:
            new_size[1] = int(new_size[0] / constraints.aspect_ratio)
        
        # Applica bounds
        if constraints.bounds:
            new_pos[0] = max(constraints.bounds.min_x, min(constraints.bounds.max_x - new_size[0], new_pos[0]))
            new_pos[1] = max(constraints.bounds.min_y, min(constraints.bounds.max_y - new_size[1], new_pos[1]))
        
        # Applica ancoraggi
        if constraints.anchors:
            for edge, anchor in constraints.anchors.items():
                if anchor.target_id in self.widget_bounds:
                    target_bounds = self.widget_bounds[anchor.target_id]
                    if edge == "left":
                        if anchor.edge == "right":
                            new_pos[0] = target_bounds[0] + target_bounds[2] + anchor.offset
                        elif anchor.edge == "left":
                            new_pos[0] = target_bounds[0] + anchor.offset
                    # Implementa altri casi di ancoraggio
        
        return tuple(new_pos), tuple(new_size)

__all__ = ['Anchor', 'Bounds', 'AdvancedConstraints', 'ConstraintManager']