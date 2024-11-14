from typing import Union

class Color:
    # Dizionario dei colori predefiniti
    NAMED_COLORS = {
        'black': '#000000',
        'white': '#FFFFFF', 
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        # ... altri colori predefiniti
    }

    def __init__(self, value: Union[str, tuple, list]):
        if isinstance(value, str):
            if value.startswith('#'):
                # Hex color
                value = value.lstrip('#')
                if len(value) == 3:
                    value = ''.join(c + c for c in value)
                self.r = int(value[0:2], 16)
                self.g = int(value[2:4], 16)
                self.b = int(value[4:6], 16)
                self.a = 255
            else:
                # Named color
                hex_value = self.NAMED_COLORS.get(value.lower())
                if hex_value:
                    self.__init__(hex_value)
                else:
                    raise ValueError("Color deve essere inizializzato con una stringa hex, nome colore, o valori RGB(A)")
        elif isinstance(value, (tuple, list)) and len(value) in (3, 4):
            self.r = value[0]
            self.g = value[1]
            self.b = value[2]
            self.a = value[3] if len(value) == 4 else 255
        else:
            raise ValueError("Color deve essere inizializzato con una stringa hex, nome colore, o valori RGB(A)")
    
    def to_hex(self) -> str:
        """Converte il colore in formato hex"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_rgba(self) -> tuple:
        """Restituisce il colore come tupla RGBA"""
        return (self.r, self.g, self.b, self.a)
    
    def lighten(self, amount: float) -> 'Color':
        """Schiarisce il colore di una certa quantità (0-1)"""
        def clamp(value):
            return max(0, min(255, value))
        
        r = clamp(int(self.r + (255 - self.r) * amount))
        g = clamp(int(self.g + (255 - self.g) * amount))
        b = clamp(int(self.b + (255 - self.b) * amount))
        
        return Color((r, g, b, self.a))
    
    def darken(self, amount: float) -> 'Color':
        """Scurisce il colore di una certa quantità (0-1)"""
        def clamp(value):
            return max(0, min(255, value))
        
        r = clamp(int(self.r * (1 - amount)))
        g = clamp(int(self.g * (1 - amount)))
        b = clamp(int(self.b * (1 - amount)))
        
        return Color((r, g, b, self.a))

    @staticmethod
    def from_hex(hex_color: str) -> 'Color':
        return Color(hex_color)
    
    @staticmethod
    def from_rgb(r: int, g: int, b: int, a: int = 255) -> 'Color':
        return Color((r, g, b, a))
    
    def to_windows_color(self) -> int:
        # Formato Windows: 0x00BBGGRR
        return self.r | (self.g << 8) | (self.b << 16)
    
    def with_alpha(self, alpha: float) -> 'Color':
        return Color((self.r, self.g, self.b, int(alpha * 255)))
    
    def __str__(self) -> str:
        if self.a == 255:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        return f"rgba({self.r},{self.g},{self.b},{self.a/255})"