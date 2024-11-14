from typing import Dict, Any, Optional, Callable, Type, Union, List
from dataclasses import dataclass
from .virtual_node import VirtualNode

@dataclass
class StyleConfig:
    """Configurazione dettagliata dello stile"""
    # Dimensioni e Layout
    width: Optional[Union[int, str]] = None
    height: Optional[Union[int, str]] = None
    padding: Optional[Union[int, str, Dict[str, int]]] = None
    margin: Optional[Union[int, str, Dict[str, int]]] = None
    
    # Bordi e Forma
    border_width: Optional[int] = None
    border_style: Optional[str] = None
    border_color: Optional[str] = None
    border_radius: Optional[Union[int, Dict[str, int]]] = None
    
    # Colori e Sfondo
    background: Optional[Union[str, Dict[str, str]]] = None
    background_gradient: Optional[Dict[str, Any]] = None
    color: Optional[str] = None
    opacity: Optional[float] = None
    
    # Ombreggiature
    box_shadow: Optional[Union[str, List[Dict[str, Any]]]] = None
    text_shadow: Optional[str] = None
    
    # Tipografia
    font_family: Optional[str] = None
    font_size: Optional[Union[int, str]] = None
    font_weight: Optional[Union[int, str]] = None
    line_height: Optional[Union[int, str]] = None
    text_align: Optional[str] = None
    letter_spacing: Optional[Union[int, str]] = None
    
    # Transizioni e Animazioni
    transition: Optional[Dict[str, Any]] = None
    animation: Optional[Dict[str, Any]] = None
    transform: Optional[str] = None
    
    # Effetti
    filter: Optional[str] = None
    backdrop_filter: Optional[str] = None
    mix_blend_mode: Optional[str] = None

@dataclass
class StateConfig:
    """Configurazione degli stati del componente"""
    hover: Optional[StyleConfig] = None
    active: Optional[StyleConfig] = None
    focus: Optional[StyleConfig] = None
    disabled: Optional[StyleConfig] = None
    pressed: Optional[StyleConfig] = None
    selected: Optional[StyleConfig] = None

@dataclass
class RenderPart:
    """Definisce una parte renderizzabile di un componente"""
    name: str
    renderer: Callable
    style: StyleConfig = None
    states: StateConfig = None
    behaviors: Dict[str, Callable] = None

@dataclass 
class ComponentConfig:
    """Configurazione completa del componente"""
    name: str
    base_style: StyleConfig
    states: StateConfig = None
    variants: Dict[str, StyleConfig] = None
    behaviors: Dict[str, Callable] = None
    parts: Dict[str, RenderPart] = None
    layout_rules: Dict[str, Any] = None
    accessibility: Dict[str, Any] = None
    
    def with_part(self, name: str, part: RenderPart) -> 'ComponentConfig':
        """Aggiunge o aggiorna una parte del componente"""
        new_config = ComponentConfig(
            name=self.name,
            base_style=self.base_style,
            states=self.states,
            variants=self.variants.copy() if self.variants else None,
            behaviors=self.behaviors.copy() if self.behaviors else None,
            parts=(self.parts or {}).copy(),
            layout_rules=self.layout_rules.copy() if self.layout_rules else None,
            accessibility=self.accessibility.copy() if self.accessibility else None
        )
        new_config.parts[name] = part
        return new_config

class CustomizableComponent:
    """Componente altamente personalizzabile"""
    def __init__(self, config: ComponentConfig):
        self.config = config
        self._style_overrides: Dict[str, Any] = {}
        self._state_overrides: Dict[str, Any] = {}
        self._behavior_overrides: Dict[str, Callable] = {}
        self._render_overrides: Dict[str, Callable] = {}
        self._part_overrides: Dict[str, Dict[str, Any]] = {}
        
    def customize_part(self, part_name: str, 
                      style: Dict[str, Any] = None,
                      states: Dict[str, Dict[str, Any]] = None,
                      behaviors: Dict[str, Callable] = None,
                      renderer: Callable = None) -> 'CustomizableComponent':
        """Personalizza una parte specifica del componente"""
        new_component = self._clone()
        if part_name not in new_component._part_overrides:
            new_component._part_overrides[part_name] = {}
            
        if style:
            new_component._part_overrides[part_name]["style"] = style
        if states:
            new_component._part_overrides[part_name]["states"] = states
        if behaviors:
            new_component._part_overrides[part_name]["behaviors"] = behaviors
        if renderer:
            new_component._part_overrides[part_name]["renderer"] = renderer
            
        return new_component
        
    def with_variant(self, variant_name: str, 
                    customize: Dict[str, Any] = None) -> 'CustomizableComponent':
        """Applica una variante con personalizzazioni opzionali"""
        if variant_name not in self.config.variants:
            return self
            
        new_component = self._clone()
        variant_style = self.config.variants[variant_name]
        new_component._style_overrides.update(vars(variant_style))
        
        if customize:
            new_component._style_overrides.update(customize)
            
        return new_component
        
    def customize_style(self, style: Dict[str, Any]) -> 'CustomizableComponent':
        """Personalizza lo stile base"""
        new_component = self._clone()
        new_component._style_overrides.update(style)
        return new_component
        
    def customize_state(self, state: str, style: Dict[str, Any]) -> 'CustomizableComponent':
        """Personalizza lo stile di uno stato specifico"""
        new_component = self._clone()
        if state not in new_component._state_overrides:
            new_component._state_overrides[state] = {}
        new_component._state_overrides[state].update(style)
        return new_component
        
    def customize_behavior(self, event: str, handler: Callable) -> 'CustomizableComponent':
        """Personalizza un comportamento"""
        new_component = self._clone()
        new_component._behavior_overrides[event] = handler
        return new_component
        
    def customize_render(self, part: str, renderer: Callable) -> 'CustomizableComponent':
        """Personalizza il rendering di una parte specifica"""
        new_component = self._clone()
        new_component._render_overrides[part] = renderer
        return new_component
        
    def _clone(self) -> 'CustomizableComponent':
        new_component = CustomizableComponent(self.config)
        new_component._style_overrides = self._style_overrides.copy()
        new_component._state_overrides = self._state_overrides.copy()
        new_component._behavior_overrides = self._behavior_overrides.copy()
        new_component._render_overrides = self._render_overrides.copy()
        new_component._part_overrides = self._part_overrides.copy()
        return new_component
        
    def render(self, props: Dict[str, Any] = None) -> VirtualNode:
        final_props = self._build_final_props(props or {})
        
        # Usa renderer personalizzato se disponibile
        if "content" in self._render_overrides:
            return self._render_overrides["content"](final_props)
            
        return VirtualNode(
            component_type=self.config.name,
            props=final_props,
            children=[]
        )
        
    def _build_final_props(self, props: Dict[str, Any]) -> Dict[str, Any]:
        final_props = {
            "style": self._merge_styles(props.get("style", {})),
            **props
        }
        
        # Applica comportamenti personalizzati
        for event, handler in self._behavior_overrides.items():
            final_props[event] = handler
            
        return final_props
        
    def _merge_styles(self, props_style: Dict[str, Any]) -> Dict[str, Any]:
        base_style = vars(self.config.base_style)
        return {
            **base_style,
            **self._style_overrides,
            **props_style
        }