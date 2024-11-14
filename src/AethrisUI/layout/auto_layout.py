from typing import List, Dict, Any, Tuple
from ..core import VirtualNode

class AutoLayout:
    @staticmethod
    def arrange_grid(widgets: List[VirtualNode], container_size: Tuple[int, int]) -> Dict[str, Dict[str, Any]]:
        """Organizza automaticamente i widget in una griglia"""
        num_widgets = len(widgets)
        cols = int(num_widgets ** 0.5)
        rows = (num_widgets + cols - 1) // cols
        
        cell_width = container_size[0] / cols
        cell_height = container_size[1] / rows
        
        layouts = {}
        for i, widget in enumerate(widgets):
            row = i // cols
            col = i % cols
            
            layouts[widget.id] = {
                "position": (col * cell_width, row * cell_height),
                "size": (cell_width * 0.9, cell_height * 0.9)  # 90% della cella per lo spacing
            }
        
        return layouts
    
    @staticmethod
    def arrange_flow(widgets: List[VirtualNode], container_size: Tuple[int, int]) -> Dict[str, Dict[str, Any]]:
        """Organizza i widget in un layout fluido"""
        current_x = 0
        current_y = 0
        row_height = 0
        layouts = {}
        
        for widget in widgets:
            widget_width = widget.props.get("preferred_width", 100)
            widget_height = widget.props.get("preferred_height", 100)
            
            if current_x + widget_width > container_size[0]:
                current_x = 0
                current_y += row_height
                row_height = 0
            
            layouts[widget.id] = {
                "position": (current_x, current_y),
                "size": (widget_width, widget_height)
            }
            
            current_x += widget_width
            row_height = max(row_height, widget_height)
        
        return layouts 