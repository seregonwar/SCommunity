from typing import Dict, Any, List
from ..core import VirtualNode
from .base import Widget
from ..styling import Style

def Container(props: Dict[str, Any]) -> VirtualNode:
    return VirtualNode(
        component_type="container",
        props={
            "direction": props.get("direction", "vertical"),
            "spacing": props.get("spacing", 10),
            "style": Style.merge(
                Style.container(),
                props.get("style", {})
            )
        },
        children=props.get("children", [])
    ) 