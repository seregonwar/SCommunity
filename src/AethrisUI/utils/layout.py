from typing import Dict, List, Tuple
from ..core import VirtualNode

def compute_layout(node: VirtualNode, 
                  container_size: Tuple[int, int], 
                  position: Tuple[int, int] = (0, 0)) -> Dict[str, Tuple[int, int]]:
    """
    Calcola il layout per un albero di nodi virtuali
    Restituisce un dizionario di posizioni per ogni nodo
    """
    layout = {}
    props = node.props
    
    if props.get("direction") == "vertical":
        current_y = position[1]
        for child in node.children:
            layout[child] = (position[0], current_y)
            current_y += child.props.get("height", 0) + props.get("spacing", 0)
    
    return layout 