from typing import Dict, Any
from ..core import VirtualNode

class Animated:
    @staticmethod
    def create(component: VirtualNode, 
               animation: Dict[str, Any],
               trigger: str = "onMount") -> VirtualNode:
        """
        Wrappa un componente con animazioni
        
        animation = {
            "from": { "opacity": 0, "transform": "translateY(20px)" },
            "to": { "opacity": 1, "transform": "translateY(0)" },
            "duration": 300,
            "easing": "easeOutCubic"
        }
        """
        return VirtualNode(
            component_type="animated",
            props={
                "animation": animation,
                "trigger": trigger
            },
            children=[component]
        ) 