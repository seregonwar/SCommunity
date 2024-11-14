from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class GridCell:
    x: int
    y: int
    occupied: bool = False
    widget_id: Optional[str] = None

class Grid:
    def __init__(self, cell_size: int = 20):
        self.cell_size = cell_size
        self.cells: List[List[GridCell]] = []
        self._init_grid(40, 30)  # Default 800x600 grid
    
    def _init_grid(self, width: int, height: int):
        self.cells = [[GridCell(x, y) for x in range(width)] for y in range(height)]
    
    def snap_to_grid(self, position: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position
        grid_x = round(x / self.cell_size) * self.cell_size
        grid_y = round(y / self.cell_size) * self.cell_size
        return (grid_x, grid_y)
    
    def is_cell_occupied(self, x: int, y: int) -> bool:
        if 0 <= y < len(self.cells) and 0 <= x < len(self.cells[0]):
            return self.cells[y][x].occupied
        return True  # Fuori dalla griglia è considerato occupato
    
    def occupy_cells(self, x: int, y: int, width: int, height: int, widget_id: str):
        for dy in range(height):
            for dx in range(width):
                if 0 <= y+dy < len(self.cells) and 0 <= x+dx < len(self.cells[0]):
                    self.cells[y+dy][x+dx].occupied = True
                    self.cells[y+dy][x+dx].widget_id = widget_id 