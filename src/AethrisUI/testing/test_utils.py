from typing import Any, Dict, List, Callable
from ..core import VirtualNode
from ..core.renderer import Renderer

class TestRenderer(Renderer):
    def __init__(self):
        self.rendered_nodes: List[VirtualNode] = []
        self.events: List[Dict[str, Any]] = []
    
    def render(self, node: VirtualNode):
        self.rendered_nodes.append(node)
    
    def simulate_event(self, event_type: str, target: VirtualNode, data: Any = None):
        self.events.append({
            "type": event_type,
            "target": target,
            "data": data
        })
        if event_type in target.props:
            target.props[event_type](data)

def render_for_test(component: Callable[[], VirtualNode]) -> TestRenderer:
    renderer = TestRenderer()
    renderer.render(component())
    return renderer 