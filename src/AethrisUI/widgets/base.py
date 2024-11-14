from typing import Dict, Any
from ..core import Component, VirtualNode

class Widget(Component):
    def __init__(self, position=(0, 0), size=(100, 30)):
        super().__init__()
        self.position = position
        self.size = size
    
    def render(self) -> VirtualNode:
        raise NotImplementedError() 