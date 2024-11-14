from typing import Callable, Dict, Any
from .virtual_node import VirtualNode
from ..hooks import use_state, use_effect

class LazyComponent:
    def __init__(self, loader: Callable):
        self.loader = loader
        self._component = None
    
    async def load(self):
        if not self._component:
            self._component = await self.loader()
        return self._component

def lazy(loader: Callable) -> LazyComponent:
    return LazyComponent(loader)

def Suspense(props: Dict[str, Any]) -> VirtualNode:
    fallback = props.get('fallback')
    children = props.get('children', [])
    
    loading, set_loading = use_state(True)
    
    async def load_children():
        for child in children:
            if isinstance(child, LazyComponent):
                await child.load()
        set_loading(False)
    
    use_effect(lambda: load_children(), [])
    
    return VirtualNode(
        component_type="suspense",
        props={"loading": loading},
        children=[fallback] if loading else children
    ) 