from typing import Dict, Any
from dataclasses import dataclass

@dataclass 
class StyleSystem:
    breakpoints: Dict[str, int] = {
        "sm": 640,
        "md": 768,
        "lg": 1024,
        "xl": 1280
    }
    theme: Dict[str, Any] = None
    
    def responsive(self, styles: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        
        # Handle base styles
        for key, value in styles.items():
            if not isinstance(value, dict):
                result[key] = value
                
        # Handle responsive styles
        for breakpoint, width in self.breakpoints.items():
            if breakpoint in styles:
                media_query = f"@media (min-width: {width}px)"
                result[media_query] = styles[breakpoint]
                
        return result
    
    def theme_aware(self, styles: Dict[str, Any]) -> Dict[str, Any]:
        if not self.theme:
            return styles
            
        result = {}
        for key, value in styles.items():
            if isinstance(value, str) and value.startswith("$"):
                theme_key = value[1:]
                if theme_key in self.theme:
                    result[key] = self.theme[theme_key]
                else:
                    result[key] = value
            else:
                result[key] = value
                
        return result