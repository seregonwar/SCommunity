from typing import Dict, Any, Type
import importlib

class Plugin:
    def initialize(self, app: Any):
        pass
    
    def cleanup(self):
        pass

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
    
    def register_plugin(self, name: str, plugin_class: Type[Plugin]):
        self._plugins[name] = plugin_class()
    
    def load_plugin(self, module_path: str):
        module = importlib.import_module(module_path)
        if hasattr(module, 'plugin'):
            plugin = getattr(module, 'plugin')
            self.register_plugin(module_path, plugin) 