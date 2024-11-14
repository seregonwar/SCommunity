from typing import Dict, Any, Type
from ..core import VirtualNode, Component

def styled(base_component: Type[Component], default_style: Dict[str, Any]):
    """
    Crea un nuovo componente con stili predefiniti
    """
    def styled_component(props=None, **kwargs):
        if isinstance(props, str):
            # Se viene passata una stringa, la trattiamo come testo
            props = {"text": props, **kwargs}
        else:
            props = props or {}
            props.update(kwargs)
            
        # Merge degli stili
        style = default_style.copy()
        if "style" in props:
            style.update(props["style"])
        props["style"] = style
        
        return base_component(props)
    
    return styled_component 