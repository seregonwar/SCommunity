from typing import Optional, Dict, Any, Type
from dataclasses import dataclass
import traceback
import sys

@dataclass
class ErrorInfo:
    error: Exception
    component: Optional[str]
    props: Optional[Dict[str, Any]]
    stack_trace: str

class ErrorBoundary:
    def __init__(self, fallback_ui: Optional[callable] = None):
        self.fallback_ui = fallback_ui
        self.error_info: Optional[ErrorInfo] = None
    
    def catch(self, error: Exception, component: str = None, props: Dict[str, Any] = None):
        self.error_info = ErrorInfo(
            error=error,
            component=component,
            props=props,
            stack_trace=traceback.format_exc()
        ) 