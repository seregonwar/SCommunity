from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Guide:
    position: int
    orientation: str  # "horizontal" o "vertical"
    strength: float = 1.0  # Forza di attrazione (0-1)

class GuideSystem:
    def __init__(self, snap_threshold: int = 10):
        self.guides: List[Guide] = []
        self.snap_threshold = snap_threshold
    
    def add_guide(self, guide: Guide):
        self.guides.append(guide)
    
    def find_snap_position(self, pos: Tuple[int, int], size: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        width, height = size
        
        for guide in self.guides:
            if guide.orientation == "vertical":
                # Snap al bordo sinistro
                if abs(x - guide.position) < self.snap_threshold:
                    x = guide.position
                # Snap al centro
                elif abs((x + width/2) - guide.position) < self.snap_threshold:
                    x = guide.position - width/2
                # Snap al bordo destro
                elif abs((x + width) - guide.position) < self.snap_threshold:
                    x = guide.position - width
            else:
                # Logica simile per guide orizzontali
                if abs(y - guide.position) < self.snap_threshold:
                    y = guide.position
                elif abs((y + height/2) - guide.position) < self.snap_threshold:
                    y = guide.position - height/2
                elif abs((y + height) - guide.position) < self.snap_threshold:
                    y = guide.position - height
        
        return (x, y) 