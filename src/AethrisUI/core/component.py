from typing import Dict
from .virtual_node import VirtualNode

class Component:
    def __init__(self):
        self.virtual_dom = None
        self.is_mounted = False
    
    def render(self) -> VirtualNode:
        raise NotImplementedError()
    
    def should_update(self, old_props: Dict, new_props: Dict) -> bool:
        return True 