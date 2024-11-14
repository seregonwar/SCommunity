from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class MagneticZone:
    x: int
    y: int
    width: int
    height: int
    strength: float = 1.0
    type: str = "snap"  # "snap", "attract", "repel"

class MagneticLayout:
    def __init__(self, attraction_radius: int = 50):
        self.zones: List[MagneticZone] = []
        self.attraction_radius = attraction_radius
    
    def add_zone(self, zone: MagneticZone):
        self.zones.append(zone)
    
    def calculate_force(self, widget_pos: Tuple[int, int], widget_size: Tuple[int, int]) -> Tuple[float, float]:
        total_force_x = 0.0
        total_force_y = 0.0
        
        widget_center = (
            widget_pos[0] + widget_size[0]/2,
            widget_pos[1] + widget_size[1]/2
        )
        
        for zone in self.zones:
            zone_center = (
                zone.x + zone.width/2,
                zone.y + zone.height/2
            )
            
            dx = zone_center[0] - widget_center[0]
            dy = zone_center[1] - widget_center[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.attraction_radius:
                force = (1 - distance/self.attraction_radius) * zone.strength
                if zone.type == "repel":
                    force = -force
                
                total_force_x += dx * force / distance if distance > 0 else 0
                total_force_y += dy * force / distance if distance > 0 else 0
        
        return (total_force_x, total_force_y) 