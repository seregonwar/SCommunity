from typing import Optional, Callable, Dict, Any
from ..core import VirtualNode
from ..styling import ModernStyle, Theme
from ..widgets import Container, Button, Text
from ..platform import Window
from .error_handler import ErrorInfo, use_error_boundary

def DefaultErrorUI(error_info: ErrorInfo) -> VirtualNode:
    window = Window.get_instance()
    
    return Container({
        "children": [
            Text("Something went wrong"),
            Container({
                "children": [
                    Text(f"Error: {str(error_info.error)}"),
                    Text(f"Component: {error_info.component}"),
                    Container({
                        "children": [
                            Text("Stack Trace:"),
                            Text(error_info.stack_trace)
                        ],
                        "style": {
                            "background": "rgba(0,0,0,0.05)",
                            "padding": "10px",
                            "border_radius": "5px",
                            "font_family": "monospace",
                            "max_height": "200px",
                            "overflow": "auto"
                        }
                    })
                ],
                "style": {
                    "padding": "20px",
                    **ModernStyle.card("glass")
                }
            }),
            Button({
                "text": "Reload Application",
                "onClick": lambda: window.reload(),
                "variant": "filled",
                "style": {
                    "margin_top": "20px"
                }
            })
        ],
        "style": {
            "padding": "20px",
            "display": "flex",
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "height": "100%",
            "background": Theme.current.background
        }
    })

class ErrorBoundary:
    def __init__(self, fallback_ui: Optional[Callable[[ErrorInfo], VirtualNode]] = None):
        self.fallback_ui = fallback_ui or DefaultErrorUI
        self.error_info: Optional[ErrorInfo] = None
    
    def wrap(self, component: Callable[[], VirtualNode]) -> Callable[[], VirtualNode]:
        @use_error_boundary(self.fallback_ui)
        def wrapped_component():
            if self.error_info:
                return self.fallback_ui(self.error_info)
            return component()
        return wrapped_component 