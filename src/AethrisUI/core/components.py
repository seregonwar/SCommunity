from typing import Dict, Any, List
from .virtual_node import VirtualNode

def Container(props: Dict[str, Any] = None) -> VirtualNode:
    """
    Componente Container base che può contenere altri elementi
    """
    return VirtualNode(
        component_type="container",
        props=props or {},
        children=props.get("children", []) if props else []
    )

def Button(props: Dict[str, Any] = None) -> VirtualNode:
    """
    Componente Button base
    """
    return VirtualNode(
        component_type="button",
        props=props or {},
        children=[]
    )

def Text(text: str = "", props: Dict[str, Any] = None) -> VirtualNode:
    """
    Componente Text base
    """
    if props is None:
        props = {}
    props["text"] = text
    
    return VirtualNode(
        component_type="text",
        props=props,
        children=[]
    ) 