from typing import Dict, Any, Callable, List
from dataclasses import dataclass

@dataclass
class MediaQuery:
    condition: Callable[[], bool]
    styles: Dict[str, Any]

class MediaQueryList:
    def __init__(self):
        self.queries: List[MediaQuery] = []
    
    def add(self, query: MediaQuery):
        self.queries.append(query)
    
    def evaluate(self) -> Dict[str, Any]:
        result = {}
        for query in self.queries:
            if query.condition():
                result.update(query.styles)
        return result

def create_media_query(min_width: int = None, max_width: int = None) -> Callable[[], bool]:
    def check() -> bool:
        from ..platform.window import Window
        current_width = Window.get_current_size()[0]
        if min_width and current_width < min_width:
            return False
        if max_width and current_width > max_width:
            return False
        return True
    return check