from typing import Dict, Any
from dataclasses import dataclass
from ..platform.color import Color

@dataclass
class Colors:
    primary: Color = Color("#007AFF")
    secondary: Color = Color("#5856D6")
    success: Color = Color("#34C759")
    warning: Color = Color("#FF9500")
    error: Color = Color("#FF3B30")
    background: Color = Color("#FFFFFF")
    surface: Color = Color("#F2F2F7")
    text: Color = Color("#000000")
    text_secondary: Color = Color("#8E8E93")

@dataclass
class Spacing:
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32

@dataclass
class Typography:
    font_family: str = "Segoe UI"
    font_size_base: int = 14
    font_size_lg: int = 16
    font_size_sm: int = 12
    font_weight_normal: str = "normal"
    font_weight_bold: str = "bold"

class Theme:
    """
    Classe singleton che gestisce il tema dell'applicazione
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Theme, cls).__new__(cls)
            cls._instance._init_default_theme()
        return cls._instance
    
    def _init_default_theme(self):
        self.colors = Colors()
        self.spacing = Spacing()
        self.typography = Typography()
    
    @classmethod
    def get_instance(cls) -> 'Theme':
        if cls._instance is None:
            cls._instance = Theme()
        return cls._instance
    
    @classmethod
    def set_theme(cls, theme_config: Dict[str, Any]):
        instance = cls.get_instance()
        
        if 'colors' in theme_config:
            for key, value in theme_config['colors'].items():
                if hasattr(instance.colors, key):
                    setattr(instance.colors, key, Color(value))
        
        if 'spacing' in theme_config:
            for key, value in theme_config['spacing'].items():
                if hasattr(instance.spacing, key):
                    setattr(instance.spacing, key, value)
        
        if 'typography' in theme_config:
            for key, value in theme_config['typography'].items():
                if hasattr(instance.typography, key):
                    setattr(instance.typography, key, value)

# Esporta un'istanza singleton
current = Theme.get_instance() 