from typing import Dict, Any, Callable, Optional, Type, List
from abc import ABC, abstractmethod
import webview
import json
import logging
from pathlib import Path
from dataclasses import dataclass
from ..utils.error_handling import ErrorBoundary
import time

logger = logging.getLogger(__name__)

@dataclass
class WebConfig:
    """Configurazione avanzata per il bridge web"""
    # Dimensioni e Layout
    width: int = 800
    height: int = 600
    min_size: tuple = (200, 200)
    max_size: Optional[tuple] = None
    
    # Comportamento Finestra
    resizable: bool = True
    fullscreen: bool = False
    frameless: bool = False
    transparent: bool = False
    
    # Stile e Aspetto
    background_color: str = "#FFFFFF"
    font_family: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    theme: str = "light"  # light/dark/system
    
    # Development
    debug: bool = False
    hot_reload: bool = False
    dev_tools: bool = False
    
    # Framework Specifico
    use_typescript: bool = False
    use_strict_mode: bool = True
    use_suspense: bool = True
    enable_concurrent: bool = True
    css_modules: bool = True
    styled_components: bool = True
    
    # Interazione
    easy_drag: bool = True
    text_select: bool = False
    context_menu: bool = False
    
    # Performance
    hardware_acceleration: bool = True
    offscreen_rendering: bool = False

class WebBridgeEvents:
    """Eventi standard del bridge"""
    READY = "bridge:ready"
    ERROR = "bridge:error"
    STATE_CHANGE = "bridge:stateChange"
    ACTION = "bridge:action"
    NAVIGATION = "bridge:navigation"

class WebBridge(ABC):
    def __init__(self, config: Optional[WebConfig] = None):
        self._window = None
        self._callbacks: Dict[str, List[Callable]] = {}
        self._api_methods: Dict[str, Callable] = {}
        self._error_boundary = ErrorBoundary()
        self.config = config or WebConfig()
        self._html_content = None
        
    @abstractmethod
    def create_component(self, code: str, props: Optional[Dict[str, Any]] = None) -> None:
        pass
        
    @abstractmethod
    def inject_api(self, api_object: Any) -> None:
        pass
    
    def expose_method(self, name: str, method: Callable):
        """Espose un metodo Python al contesto web"""
        self._api_methods[name] = method
        
    def invoke_js(self, code: str) -> Any:
        """Esegue codice JavaScript nella finestra web"""
        if self._window:
            try:
                return self._window.evaluate_js(code)
            except Exception as e:
                logger.error(f"Error executing JavaScript: {e}")
                self._error_boundary.catch(e)
        return None
        
    def on(self, event: str, callback: Callable):
        """Registra un handler per un evento"""
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
        
    def off(self, event: str, callback: Callable):
        """Rimuove un handler per un evento"""
        if event in self._callbacks:
            self._callbacks[event].remove(callback)
        
    def emit(self, event: str, data: Any = None):
        """Emette un evento al contesto web"""
        if self._window:
            try:
                js_code = f"""
                window.dispatchEvent(new CustomEvent('{event}', {{
                    detail: {json.dumps(data)},
                    bubbles: true,
                    cancelable: true
                }}));
                """
                self._window.evaluate_js(js_code)
            except Exception as e:
                logger.error(f"Error emitting event {event}: {e}")
                self._error_boundary.catch(e)
    
    def _handle_event(self, event: str, data: Any = None):
        """Gestisce gli eventi interni del bridge"""
        if event in self._callbacks:
            for callback in self._callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event}: {e}")
                    self._error_boundary.catch(e)
    
    def load_html(self, html: str):
        """Memorizza l'HTML da caricare"""
        self._html_content = html
    
    def load_file(self, path: Path):
        """Carica un file HTML con supporto hot reload"""
        if self.config.hot_reload:
            try:
                self._setup_hot_reload(path)
            except ImportError:
                logger.warning(
                    "Hot reload richiede il pacchetto watchdog. "
                    "Installa con: pip install aethris-ui[web]"
                )
                
        with open(path) as f:
            self.load_html(f.read())
    
    def _setup_hot_reload(self, path: Path):
        """Configura il hot reload usando watchdog"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class ReloadHandler(FileSystemEventHandler):
                def __init__(self, bridge):
                    self.bridge = bridge
                    self._last_reload = 0
                    self._reload_delay = 0.5  # secondi
                    
                def on_modified(self, event):
                    current_time = time.time()
                    if (str(event.src_path) == str(path) and 
                        current_time - self._last_reload > self._reload_delay):
                        try:
                            with open(path) as f:
                                self.bridge.load_html(f.read())
                            self._last_reload = current_time
                            logger.debug(f"Hot reload: {path}")
                        except Exception as e:
                            logger.error(f"Hot reload failed: {e}")
            
            observer = Observer()
            observer.schedule(ReloadHandler(self), str(path.parent), recursive=False)
            observer.start()
            logger.info("Hot reload enabled")
            
            # Registra l'observer per il cleanup
            self._hot_reload_observer = observer
            
        except ImportError as e:
            raise ImportError(
                "Hot reload requires watchdog package. "
                "Install with: pip install aethris-ui[web]"
            ) from e
    
    def cleanup(self):
        """Pulisce le risorse"""
        if hasattr(self, '_hot_reload_observer'):
            self._hot_reload_observer.stop()
            self._hot_reload_observer.join()
            
    def __del__(self):
        """Assicura la pulizia delle risorse"""
        self.cleanup()
    
    def run(self, debug: bool = None):
        """Avvia l'applicazione web"""
        if debug is None:
            debug = self.config.debug
            
        if not self._html_content:
            raise ValueError("No HTML content to display")
            
        try:
            # Crea la finestra con l'HTML memorizzato
            window = webview.create_window(
                'Web Window',
                html=self._html_content,
                js_api=self,
                width=self.config.width,
                height=self.config.height,
                resizable=self.config.resizable,
                fullscreen=self.config.fullscreen,
                min_size=self.config.min_size
            )
            
            # Avvia webview in modalità debug se richiesto
            webview.start(debug=debug)
            
        except Exception as e:
            logger.error(f"Failed to start window: {e}")
            raise
    