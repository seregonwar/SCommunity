from dataclasses import dataclass
from typing import Tuple

@dataclass
class Event:
    pass

@dataclass
class MouseEvent(Event):
    position: Tuple[int, int]
    button: int
    pressed: bool

@dataclass
class KeyEvent(Event):
    key: str
    pressed: bool 