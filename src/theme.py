class Theme:
    _current = None  # Attributo privato per memorizzare l'istanza corrente
    
    @classmethod
    def get_current(cls):
        if cls._current is None:
            raise RuntimeError("Theme not initialized. Call Theme.set_current() first.")
        return cls._current
    
    @classmethod
    def set_current(cls, theme):
        cls._current = theme
    
    # Definiamo current come proprietà di classe usando un descriptor
    class CurrentThemeDescriptor:
        def __get__(self, obj, objtype=None):
            return objtype.get_current()
    
    current = CurrentThemeDescriptor()
    
    def __init__(self, name: str, colors: dict, fonts: dict):
        self.name = name
        # Importiamo Color solo quando serve
        from .platform.color import Color
        self.colors = {k: Color.from_hex(v) for k, v in colors.items()}
        self.fonts = fonts
        
        # Imposta questa istanza come tema corrente
        Theme.set_current(self)
