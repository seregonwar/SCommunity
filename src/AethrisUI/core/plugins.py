from typing import Protocol, Dict, Any

class UIPlugin(Protocol):
    def initialize(self, app: Any) -> None: ...
    def cleanup(self) -> None: ...
    def get_components(self) -> Dict[str, Any]: ...
    def get_hooks(self) -> Dict[str, Any]: ...

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, UIPlugin] = {}
        self._components: Dict[str, Any] = {}
        self._hooks: Dict[str, Any] = {}
    
    def register_plugin(self, name: str, plugin: UIPlugin):
        self._plugins[name] = plugin
        plugin.initialize(self)
        
        # Registra componenti e hooks del plugin
        self._components.update(plugin.get_components())
        self._hooks.update(plugin.get_hooks()) 