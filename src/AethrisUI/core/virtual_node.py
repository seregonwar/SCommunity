from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .state import State

@dataclass
class VirtualNode:
    """
    Rappresenta un nodo virtuale nell'albero dei componenti
    """
    component_type: str
    props: Dict[str, Any]
    children: Optional[List['VirtualNode']] = None
    
    def __post_init__(self):
        """
        Inizializza i valori di default dopo la creazione dell'istanza
        """
        if self.children is None:
            self.children = []
            
        # Se ci sono children nei props, spostali nella lista children
        if "children" in self.props:
            if isinstance(self.props["children"], list):
                self.children.extend(self.props["children"])
            else:
                self.children.append(self.props["children"])
            del self.props["children"]
    state: Optional[State] = None 