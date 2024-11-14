from typing import Dict, Any, Callable, Optional, List
from ..web.react_bridge import ReactBridge
import json

class ReactHooks:
    """Generatore di hook React"""
    
    @staticmethod
    def use_state(initial_state: Any) -> str:
        return f"""
        const [state, setState] = React.useState({json.dumps(initial_state)});
        """
    
    @staticmethod
    def use_effect(effect: str, dependencies: Optional[List[str]] = None) -> str:
        deps = f"[{', '.join(dependencies)}]" if dependencies else "[]"
        return f"""
        React.useEffect(() => {{
            {effect}
        }}, {deps});
        """
    
    @staticmethod
    def use_python_method(method_name: str) -> str:
        return f"""
        const {method_name} = async (...args) => {{
            const python = usePython();
            return await python.invoke('{method_name}', ...args);
        }};
        """
    
    @staticmethod
    def use_python_event(event_name: str) -> str:
        return f"""
        const handle_{event_name} = React.useCallback((callback) => {{
            const python = usePython();
            return python.on('{event_name}', callback);
        }}, []);
        """

class ReactComponent:
    """Generatore di componenti React"""
    
    def __init__(self, name: str):
        self.name = name
        self.hooks: List[str] = []
        self.render: str = ""
        self.styles: List[str] = []
        
    def add_hook(self, hook: str) -> 'ReactComponent':
        self.hooks.append(hook)
        return self
        
    def set_render(self, render: str) -> 'ReactComponent':
        self.render = render
        return self
        
    def add_style(self, style: str) -> 'ReactComponent':
        self.styles.append(style)
        return self
        
    def build(self) -> str:
        return f"""
        const {self.name} = (props) => {{
            {self._build_hooks()}
            {self._build_styles()}
            
            return (
                {self.render}
            );
        }};
        """
    
    def _build_hooks(self) -> str:
        return "\n".join(self.hooks)
        
    def _build_styles(self) -> str:
        return "\n".join(self.styles) 