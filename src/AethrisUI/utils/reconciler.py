from typing import Dict, Any, Optional
from ..core import VirtualNode

def reconcile(old_node: Optional[VirtualNode], 
             new_node: Optional[VirtualNode], 
             patches: Dict[str, Any]) -> None:
    """
    Confronta il vecchio e il nuovo albero virtuale
    e genera le patch necessarie per l'aggiornamento
    """
    if old_node is None and new_node is not None:
        patches["create"] = new_node
    elif old_node is not None and new_node is None:
        patches["delete"] = old_node
    elif old_node is not None and new_node is not None:
        if old_node.component_type != new_node.component_type:
            patches["replace"] = new_node
        else:
            if old_node.props != new_node.props:
                patches["update"] = new_node.props 