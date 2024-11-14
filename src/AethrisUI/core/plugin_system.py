from typing import Dict, Any, Type, Protocol, Optional
from abc import ABC, abstractmethod
import importlib
import logging

logger = logging.getLogger(__name__)

class PluginInterface(Protocol):
    def initialize(self) -> None: ...
    def cleanup(self) -> None: ...
    def get_components(self) -> Dict[str, Any]: ...
    def get_hooks(self) -> Dict[str, Any]: ...
    def get_middleware(self) -> Dict[str, Any]: ...

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, PluginInterface] = {}
        self._components: Dict[str, Any] = {}
        self._hooks: Dict[str, Any] = {}
        self._middleware: Dict[str, Any] = {}
        
    def register(self, name: str, plugin: PluginInterface):
        """Registra un nuovo plugin"""
        try:
            plugin.initialize()
            self._plugins[name] = plugin
            
            # Registra componenti, hooks e middleware
            self._components.update(plugin.get_components())
            self._hooks.update(plugin.get_hooks())
            self._middleware.update(plugin.get_middleware())
            
            logger.info(f"Plugin {name} registered successfully")
        except Exception as e:
            logger.error(f"Failed to register plugin {name}: {e}")
            raise 