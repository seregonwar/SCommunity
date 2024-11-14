from typing import Optional, Callable, Dict, Any, List
from dataclasses import dataclass
import traceback
import sys
import logging

@dataclass
class ErrorInfo:
    error: Exception
    component: Optional[str] = None
    stack_trace: str = ""
    additional_info: Dict[str, Any] = None

class ErrorHandler:
    _instance = None
    _error_listeners: List[Callable[[ErrorInfo], None]] = []
    _fallback_ui: Optional[Callable[[ErrorInfo], Any]] = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ErrorHandler()
        return cls._instance
    
    def set_fallback_ui(self, fallback: Callable[[ErrorInfo], Any]):
        self._fallback_ui = fallback
    
    def add_error_listener(self, listener: Callable[[ErrorInfo], None]):
        self._error_listeners.append(listener)
    
    def handle_error(self, error: Exception, component: Optional[str] = None, 
                    additional_info: Dict[str, Any] = None) -> Any:
        error_info = ErrorInfo(
            error=error,
            component=component,
            stack_trace=traceback.format_exc(),
            additional_info=additional_info or {}
        )
        
        # Log dell'errore
        logging.error(f"Error in component {component}: {str(error)}")
        logging.error(error_info.stack_trace)
        
        # Notifica i listener
        for listener in self._error_listeners:
            try:
                listener(error_info)
            except Exception as e:
                logging.error(f"Error in error listener: {str(e)}")
        
        # Ritorna l'UI di fallback se disponibile
        if self._fallback_ui:
            try:
                return self._fallback_ui(error_info)
            except Exception as fallback_error:
                logging.error(f"Error in fallback UI: {str(fallback_error)}")
        
        # Se non c'è fallback UI, rilancia l'errore
        raise error

def use_error_boundary(fallback_ui: Optional[Callable[[ErrorInfo], Any]] = None):
    """Hook per gestire gli errori nei componenti"""
    error_handler = ErrorHandler.get_instance()
    if fallback_ui:
        error_handler.set_fallback_ui(fallback_ui)
    
    def decorator(component_fn):
        def wrapped(*args, **kwargs):
            try:
                return component_fn(*args, **kwargs)
            except Exception as e:
                return error_handler.handle_error(
                    e, 
                    component=component_fn.__name__,
                    additional_info={"args": args, "kwargs": kwargs}
                )
        return wrapped
    return decorator 