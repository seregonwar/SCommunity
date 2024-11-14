from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from ..core import VirtualNode

@dataclass
class EventListener:
    event_type: str
    callback: Callable
    options: Dict[str, Any] = None

@dataclass
class EventHandler:
    callback: Callable
    priority: int = 0

class EventSystem:
    def __init__(self):
        self._listeners: Dict[VirtualNode, List[EventListener]] = {}
        self._capture_phase_listeners: Dict[str, List[Callable]] = {}
        self._bubble_phase_listeners: Dict[str, List[Callable]] = {}
        self._mouse_position = (0, 0)
        self._hovered_elements = set()
        self._handlers: Dict[str, List[EventHandler]] = {}
    
    def add_listener(self, node: VirtualNode, event_type: str, callback: Callable, 
                    options: Dict[str, Any] = None):
        if node not in self._listeners:
            self._listeners[node] = []
        
        listener = EventListener(event_type, callback, options or {})
        self._listeners[node].append(listener)
        
        if options and options.get("capture"):
            if event_type not in self._capture_phase_listeners:
                self._capture_phase_listeners[event_type] = []
            self._capture_phase_listeners[event_type].append(callback)
    
    def dispatch_event(self, event_type: str, target: VirtualNode, event_data: Any = None):
        # Fase di cattura (dall'alto verso il basso)
        if event_type in self._capture_phase_listeners:
            for callback in self._capture_phase_listeners[event_type]:
                callback(event_data)
        
        # Fase target
        if target in self._listeners:
            for listener in self._listeners[target]:
                if listener.event_type == event_type:
                    listener.callback(event_data)
        
        # Fase di bubbling (dal basso verso l'alto)
        if event_type in self._bubble_phase_listeners:
            for callback in self._bubble_phase_listeners[event_type]:
                callback(event_data)
    
    def handle_mouse_move(self, x: int, y: int):
        self._mouse_position = (x, y)
        
        # Trova gli elementi sotto il cursore
        current_hovered = set()
        for element, bounds in self._element_bounds.items():
            if self._is_point_inside(bounds, (x, y)):
                current_hovered.add(element)
        
        # Gestisci eventi mouseenter/mouseleave
        for element in current_hovered - self._hovered_elements:
            self._trigger_event(element, "mouseenter")
        
        for element in self._hovered_elements - current_hovered:
            self._trigger_event(element, "mouseleave")
        
        self._hovered_elements = current_hovered 
    
    def on(self, event: str, callback: Callable, priority: int = 0):
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(EventHandler(callback, priority))
        self._handlers[event].sort(key=lambda h: h.priority, reverse=True)