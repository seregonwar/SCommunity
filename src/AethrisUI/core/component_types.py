from typing import Any, Dict, Type
from dataclasses import dataclass
from .virtual_node import VirtualNode

@dataclass
class ComponentType:
    is_client: bool = False
    is_server: bool = False
    is_static: bool = False

def client_component(component_class: Type) -> Type:
    """Decorator per marcare un componente come client-side"""
    component_class._component_type = ComponentType(is_client=True)
    return component_class

def server_component(component_class: Type) -> Type:
    """Decorator per marcare un componente come server-side"""
    component_class._component_type = ComponentType(is_server=True)
    return component_class

def static_component(component_class: Type) -> Type:
    """Decorator per marcare un componente come statico"""
    component_class._component_type = ComponentType(is_static=True)
    return component_class 