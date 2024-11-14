from typing import List, Dict, Any
from ..core import VirtualNode

class FlexContainer:
    @staticmethod
    def create(children: List[VirtualNode], style: Dict[str, Any] = None) -> VirtualNode:
        base_style = {
            "display": "flex",
            "flex_direction": "row",
            "justify_content": "flex_start",
            "align_items": "stretch",
            "flex_wrap": "nowrap",
            "gap": "0px"
        }
        
        if style:
            base_style.update(style)
            
        return VirtualNode(
            component_type="container",
            props={"style": base_style},
            children=children
        ) 