from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class ThemeDefinition:
    colors: Dict[str, str]
    typography: Dict[str, Any]
    spacing: Dict[str, int]
    breakpoints: Dict[str, int]
    components: Dict[str, Any]

class ThemeProvider:
    def __init__(self):
        self._themes: Dict[str, ThemeDefinition] = {}
        self._active_theme: Optional[str] = None
    
    def load_theme(self, path: Path):
        with open(path) as f:
            theme_data = json.load(f)
        name = theme_data.pop("name")
        self._themes[name] = ThemeDefinition(**theme_data)
    
    def set_active_theme(self, name: str):
        if name not in self._themes:
            raise ValueError(f"Theme {name} not found")
        self._active_theme = name 