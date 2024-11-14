from typing import Dict, Any
from .virtual_node import VirtualNode

class Portal:
    _targets: Dict[str, Any] = {}
    
    @classmethod
    def create_target(cls, name: str, target: Any):
        cls._targets[name] = target
    
    @classmethod
    def render_to(cls, target_name: str, node: VirtualNode):
        if target_name in cls._targets:
            from .renderer import Renderer
            renderer = Renderer(cls._targets[target_name])
            renderer.render(node) 