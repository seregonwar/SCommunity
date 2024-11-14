from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class Context:
    name: str
    default_value: Any

class ContextProvider:
    _contexts: Dict[str, Any] = {}
    
    @classmethod
    def provide(cls, context: Context, value: Any):
        cls._contexts[context.name] = value
    
    @classmethod
    def get(cls, context: Context) -> Any:
        return cls._contexts.get(context.name, context.default_value)

def create_context(name: str, default_value: Any = None) -> Context:
    return Context(name=name, default_value=default_value)

def use_context(context: Context) -> Any:
    return ContextProvider.get(context) 