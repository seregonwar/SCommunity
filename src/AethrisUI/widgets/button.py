from typing import Dict, Any, List, Optional
from ..core import VirtualNode
from ..platform.color import Color
from ..animation.effects import ButtonEffects, RippleEffect, ElevationEffect
from ..styling.theme import Theme
from ..widgets.container import Container
from ..widgets.text import Text

class ButtonComponent:
    def __init__(self, props):
        self.props = props
        self._ripples: List[RippleEffect] = []
        self._elevation = ElevationEffect(1, Color("#000000"))
        self._is_hovered = False
        self._is_pressed = False
        self._setup_styles()
    
    def _setup_styles(self):
        variant = self.props.get("variant", "primary")
        theme = Theme.get_current()
        self.base_color = theme.colors.get(variant, Color("#007AFF"))
        
        style = self.props.get("style", {})
        
        self.base_style = {
            "position": "relative",
            "padding": "10px 20px",
            "border_radius": "8px",
            "border": "none",
            "outline": "none",
            "font_size": "16px",
            "font_weight": "500",
            "cursor": "pointer",
            "user_select": "none",
            "overflow": "hidden",
            "background": style.get("background", self.base_color.to_hex()),
            "color": style.get("color", "#FFFFFF"),
            "transition": ButtonEffects.get_transitions(),
            "box_shadow": self._elevation.get_shadow(),
            **style
        }
    
    def render(self) -> VirtualNode:
        current_style = self._get_current_style()
        
        ripple_elements = [self._create_ripple_element(ripple) 
                          for ripple in self._ripples]
        
        return VirtualNode(
            component_type="button",
            props={
                **self.props,
                "style": current_style,
                "onMouseEnter": self._handle_mouse_enter,
                "onMouseLeave": self._handle_mouse_leave,
                "onMouseDown": self._handle_mouse_down,
                "onMouseUp": self._handle_mouse_up,
            },
            children=[
                Container({
                    "style": {
                        "position": "absolute",
                        "top": 0,
                        "left": 0,
                        "right": 0,
                        "bottom": 0,
                        "overflow": "hidden",
                        "border_radius": "inherit"
                    },
                    "children": ripple_elements
                }),
                Text(self.props.get("text", ""))
            ]
        )
    
    def _get_current_style(self) -> Dict[str, Any]:
        style = self.base_style.copy()
        
        if self._is_pressed:
            self._elevation.level = 0
            style.update({
                "transform": "scale(0.98)",
                "background": self.base_color.darken(0.1).to_hex(),
                "box_shadow": self._elevation.get_shadow()
            })
        elif self._is_hovered:
            self._elevation.level = 2
            style.update({
                "transform": "translateY(-1px)",
                "background": self.base_color.lighten(0.1).to_hex(),
                "box_shadow": self._elevation.get_shadow()
            })
        
        return style
    
    def _create_ripple_element(self, ripple: RippleEffect) -> VirtualNode:
        size = ripple.size * 2
        return Container({
            "style": {
                "position": "absolute",
                "left": f"{ripple.x - size/2}px",
                "top": f"{ripple.y - size/2}px",
                "width": f"{size}px",
                "height": f"{size}px",
                "background": f"rgba(255,255,255,{ripple.opacity})",
                "border_radius": "50%",
                "transform": "scale(1)",
                "pointer_events": "none"
            }
        })
    
    def _handle_mouse_enter(self, e):
        self._is_hovered = True
        if self._window:
            self._window.render(self.render())
    
    def _handle_mouse_leave(self, e):
        self._is_hovered = False
        self._is_pressed = False
        if self._window:
            self._window.render(self.render())
    
    def _handle_mouse_down(self, e):
        self._is_pressed = True
        ripple = RippleEffect(e.x, e.y)
        self._ripples.append(ripple)
        if self._window:
            self._window.render(self.render())
    
    def _handle_mouse_up(self, e):
        self._is_pressed = False
        if self._window:
            self._window.render(self.render())

def Button(props: Dict[str, Any]) -> VirtualNode:
    return ButtonComponent(props).render()