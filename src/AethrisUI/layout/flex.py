from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from ..core import VirtualNode

@dataclass
class FlexItem:
    node: VirtualNode
    grow: float = 0
    shrink: float = 1
    basis: float = 0
    align_self: str = "auto"

class FlexLayout:
    def __init__(self, direction: str = "row", wrap: bool = False,
                 justify_content: str = "flex-start", align_items: str = "stretch"):
        self.direction = direction
        self.wrap = wrap
        self.justify_content = justify_content
        self.align_items = align_items
        self.items: List[FlexItem] = []
    
    def add_item(self, item: FlexItem):
        self.items.append(item)
    
    def compute_layout(self, container_size: Tuple[int, int]) -> Dict[VirtualNode, Tuple[int, int]]:
        positions = {}
        available_space = container_size[0] if self.direction == "row" else container_size[1]
        
        # Calcola lo spazio totale richiesto e il totale dei fattori di crescita
        total_basis = sum(item.basis for item in self.items)
        total_grow = sum(item.grow for item in self.items)
        
        # Distribuisci lo spazio extra in base ai fattori di crescita
        extra_space = max(0, available_space - total_basis)
        current_position = 0
        
        for item in self.items:
            size = item.basis
            if total_grow > 0 and item.grow > 0:
                size += (extra_space * item.grow) / total_grow
            
            if self.direction == "row":
                positions[item.node] = (current_position, 0)
            else:
                positions[item.node] = (0, current_position)
            
            current_position += size
        
        return positions 