from typing import Dict, Any, Optional, Union, Type
from dataclasses import dataclass, field
from ..platform.color import Color

@dataclass
class ThemeTokens:
    """Tokens base per il tema"""
    colors: Dict[str, Color] = field(default_factory=dict)
    spacing: Dict[str, Union[int, str]] = field(default_factory=dict)
    typography: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    shadows: Dict[str, str] = field(default_factory=dict)
    borders: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    transitions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    breakpoints: Dict[str, int] = field(default_factory=dict)
    radii: Dict[str, Union[int, str]] = field(default_factory=dict)
    gradients: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def extend(self, overrides: Dict[str, Any]) -> 'ThemeTokens':
        """Estende i tokens con nuovi valori"""
        new_tokens = ThemeTokens()
        for key, value in vars(self).items():
            if key in overrides:
                if isinstance(value, dict):
                    new_value = {**value, **overrides[key]}
                else:
                    new_value = overrides[key]
                setattr(new_tokens, key, new_value)
            else:
                setattr(new_tokens, key, value)
        return new_tokens

@dataclass
class ComponentStyle:
    """Stile base per un componente"""
    base: Dict[str, Any] = field(default_factory=dict)
    variants: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    sizes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def extend(self, overrides: Dict[str, Any]) -> 'ComponentStyle':
        """Estende lo stile con nuovi valori"""
        new_style = ComponentStyle()
        new_style.base = {**self.base, **overrides.get('base', {})}
        new_style.variants = {**self.variants, **overrides.get('variants', {})}
        new_style.states = {**self.states, **overrides.get('states', {})}
        new_style.sizes = {**self.sizes, **overrides.get('sizes', {})}
        return new_style

class ThemeBuilder:
    """Builder per creare temi personalizzati"""
    def __init__(self):
        self.tokens = ThemeTokens()
        self.components: Dict[str, ComponentStyle] = {}
        
    def with_tokens(self, tokens: Dict[str, Any]) -> 'ThemeBuilder':
        self.tokens = self.tokens.extend(tokens)
        return self
        
    def with_component(self, name: str, style: Dict[str, Any]) -> 'ThemeBuilder':
        if name in self.components:
            self.components[name] = self.components[name].extend(style)
        else:
            self.components[name] = ComponentStyle(**style)
        return self
        
    def build(self) -> 'Theme':
        return Theme(self.tokens, self.components)

class Theme:
    """Gestore principale del tema"""
    def __init__(self, tokens: ThemeTokens, components: Dict[str, ComponentStyle]):
        self.tokens = tokens
        self.components = components
        
    @classmethod
    def create(cls) -> ThemeBuilder:
        return ThemeBuilder()
        
    def get_component_style(self, 
                          component: str, 
                          variant: Optional[str] = None,
                          size: Optional[str] = None,
                          state: Optional[str] = None) -> Dict[str, Any]:
        """Ottiene lo stile completo per un componente"""
        if component not in self.components:
            return {}
            
        style = self.components[component]
        result = style.base.copy()
        
        if variant and variant in style.variants:
            result.update(style.variants[variant])
            
        if size and size in style.sizes:
            result.update(style.sizes[size])
            
        if state and state in style.states:
            result.update(style.states[state])
            
        return result 