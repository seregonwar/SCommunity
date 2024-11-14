from typing import Dict, Any, Optional, Type, Union, List
from .bridge_core import WebBridge, WebConfig
import json
import logging
from pathlib import Path
from ..styling.advanced_theme import Theme, ThemeBuilder

logger = logging.getLogger(__name__)

class ReactConfig(WebConfig):
    """Configurazione specifica per React"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_strict_mode: bool = True
        self.use_suspense: bool = True
        self.enable_concurrent: bool = True
        self.dev_tools: bool = True
        self.use_typescript: bool = False
        self.css_modules: bool = True
        self.styled_components: bool = True
        self.theme: Optional[Theme] = None
        self.source_path: Optional[Path] = None

class ReactBridge(WebBridge):
    def __init__(self, config: Optional[ReactConfig] = None):
        super().__init__(config or ReactConfig())
        self._theme = config.theme if config and config.theme else self._create_default_theme()
        self._dependencies = []
        self._inject_dependencies()
        
    def _create_default_theme(self) -> Theme:
        """Crea un tema di default per React"""
        return ThemeBuilder() \
            .with_tokens({
                "colors": {
                    "primary": "#0D6EFD",
                    "secondary": "#6C757D",
                    "success": "#198754",
                    "error": "#DC3545",
                    "warning": "#FFC107",
                    "info": "#0DCAF0",
                    "light": "#F8F9FA",
                    "dark": "#212529",
                    "background": "#FFFFFF",
                    "surface": "#F8F9FA",
                    "text": "#212529",
                    "text_secondary": "#6C757D"
                },
                "spacing": {
                    "xs": "0.25rem",
                    "sm": "0.5rem",
                    "md": "1rem",
                    "lg": "1.5rem",
                    "xl": "2rem"
                },
                "typography": {
                    "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                    "fontSize": {
                        "xs": "0.75rem",
                        "sm": "0.875rem",
                        "md": "1rem",
                        "lg": "1.125rem",
                        "xl": "1.25rem"
                    },
                    "fontWeight": {
                        "normal": "400",
                        "medium": "500",
                        "semibold": "600",
                        "bold": "700"
                    },
                    "lineHeight": {
                        "tight": "1.25",
                        "normal": "1.5",
                        "relaxed": "1.75"
                    }
                },
                "shadows": {
                    "sm": "0 1px 2px rgba(0,0,0,0.05)",
                    "md": "0 4px 6px rgba(0,0,0,0.1)",
                    "lg": "0 10px 15px rgba(0,0,0,0.1)",
                    "xl": "0 20px 25px rgba(0,0,0,0.15)",
                    "inner": "inset 0 2px 4px rgba(0,0,0,0.05)"
                },
                "radii": {
                    "sm": "0.25rem",
                    "md": "0.375rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
                },
                "transitions": {
                    "default": {
                        "duration": "200ms",
                        "timing": "cubic-bezier(0.4, 0, 0.2, 1)"
                    },
                    "slow": {
                        "duration": "300ms",
                        "timing": "cubic-bezier(0.4, 0, 0.2, 1)"
                    },
                    "fast": {
                        "duration": "150ms",
                        "timing": "cubic-bezier(0.4, 0, 0.2, 1)"
                    }
                },
                "breakpoints": {
                    "sm": "640px",
                    "md": "768px",
                    "lg": "1024px",
                    "xl": "1280px"
                }
            }) \
            .with_component("button", {
                "base": {
                    "padding": "0.5rem 1rem",
                    "borderRadius": "0.375rem",
                    "fontSize": "1rem",
                    "fontWeight": "500",
                    "transition": "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
                },
                "variants": {
                    "solid": {
                        "background": "$colors.primary",
                        "color": "white",
                        "border": "none"
                    },
                    "outline": {
                        "background": "transparent",
                        "color": "$colors.primary",
                        "border": "1px solid $colors.primary"
                    }
                },
                "states": {
                    "hover": {
                        "transform": "translateY(-1px)",
                        "boxShadow": "$shadows.md"
                    },
                    "active": {
                        "transform": "translateY(1px)",
                        "boxShadow": "$shadows.sm"
                    }
                }
            }) \
            .build()
    
    def _setup_react_environment(self):
        """Configura l'ambiente React dopo che la finestra è stata creata"""
        if self._window:
            if self.config.dev_tools:
                self._setup_dev_tools()
                
            if self.config.hot_reload and self.config.source_path:
                self._setup_hot_reload(self.config.source_path)
    
    def create_component(self, code: str, props: Optional[Dict[str, Any]] = None):
        """Crea e renderizza un componente React"""
        html = self._generate_html(code, props)
        self.load_html(html)
    
    def _inject_dependencies(self):
        """Prepara le dipendenze React necessarie"""
        self._dependencies = [
            "https://unpkg.com/react@18/umd/react.development.js",
            "https://unpkg.com/react-dom@18/umd/react-dom.development.js",
            "https://unpkg.com/@babel/standalone/babel.min.js"
        ]
        
        if self.config.dev_tools:
            self._dependencies.append("http://localhost:8097")
    
    def _setup_dev_tools(self):
        """Configura React DevTools se la finestra è inizializzata"""
        if not self._window:
            return
            
        js_code = """
        if (process.env.NODE_ENV === 'development') {
            try {
                const devTools = require('react-devtools');
                devTools.connect();
                console.log('React DevTools connected');
            } catch (e) {
                console.warn('React DevTools not available:', e);
            }
        }
        """
        self.invoke_js(js_code)
    
    def _generate_html(self, code: str, props: Optional[Dict[str, Any]] = None) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>React Calculator</title>
            <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
            <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background-color: {self.config.background_color};
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="text/babel">
                {code}
                
                const root = ReactDOM.createRoot(document.getElementById('root'));
                root.render(
                    <App />
                );
            </script>
        </body>
        </html>
        """
    
    def _generate_dependencies(self) -> str:
        return "\n".join(
            f'<script src="{dep}"></script>'
            for dep in self._dependencies
        )
    
    def _generate_bridge_api(self) -> str:
        return """
        const createPythonBridge = () => {
            const bridge = {
                async invoke(method, ...args) {
                    try {
                        const result = await window.pywebview.api.invoke(method, ...args);
                        return JSON.parse(result);
                    } catch (error) {
                        console.error('Bridge error:', error);
                        throw error;
                    }
                },
                
                on(event, callback) {
                    window.addEventListener(event, (e) => callback(e.detail));
                    return () => window.removeEventListener(event, callback);
                },
                
                emit(event, data) {
                    window.pywebview.api.emit(event, JSON.stringify(data));
                }
            };
            
            return Object.freeze(bridge);
        };

        const PythonContext = React.createContext(null);
        
        const usePython = () => {
            const bridge = React.useContext(PythonContext);
            if (!bridge) {
                throw new Error('usePython must be used within PythonProvider');
            }
            return bridge;
        };
        
        const PythonProvider = ({ children }) => {
            const bridge = React.useMemo(createPythonBridge, []);
            return (
                <PythonContext.Provider value={bridge}>
                    {children}
                </PythonContext.Provider>
            );
        };
        """
    
    def _generate_styled_components(self) -> str:
        """Genera i componenti stilizzati di base"""
        # Usa gli stessi dati del tema
        theme_data = {
            "colors": {k: v.to_hex() if hasattr(v, 'to_hex') else v 
                      for k, v in self._theme.tokens.colors.items()},
            "spacing": self._theme.tokens.spacing,
            "typography": self._theme.tokens.typography,
            "shadows": self._theme.tokens.shadows,
            "radii": self._theme.tokens.radii,
            "transitions": self._theme.tokens.transitions
        }
        
        return f"""
        const {{ styled, css, keyframes, ThemeProvider }} = window.styled;
        
        // Definisci il tema globale
        const defaultTheme = {json.dumps(theme_data)};
        
        // Componenti di base stilizzati
        const BaseButton = styled.button`
            padding: ${{props => props.theme.spacing.md}};
            border-radius: ${{props => props.theme.radii.md}};
            border: none;
            background: ${{props => props.theme.colors.primary}};
            color: white;
            font-family: ${{props => props.theme.typography.fontFamily}};
            font-size: ${{props => props.theme.typography.fontSize.md}};
            cursor: pointer;
            transition: ${{props => props.theme.transitions.default.duration}} 
                       ${{props => props.theme.transitions.default.timing}};
            
            &:hover {{
                transform: translateY(-2px);
                box-shadow: ${{props => props.theme.shadows.md}};
            }}
            
            &:active {{
                transform: translateY(1px);
                box-shadow: ${{props => props.theme.shadows.sm}};
            }}
        `;
        
        const BaseInput = styled.input`
            padding: ${{props => props.theme.spacing.sm}} ${{props => props.theme.spacing.md}};
            border: 1px solid ${{props => props.theme.colors.secondary}};
            border-radius: ${{props => props.theme.radii.sm}};
            font-family: ${{props => props.theme.typography.fontFamily}};
            font-size: ${{props => props.theme.typography.fontSize.md}};
            
            &:focus {{
                outline: none;
                border-color: ${{props => props.theme.colors.primary}};
                box-shadow: 0 0 0 2px ${{props => props.theme.colors.primary}}33;
            }}
        `;
        
        const BaseContainer = styled.div`
            padding: ${{props => props.theme.spacing.lg}};
            background: white;
            border-radius: ${{props => props.theme.radii.lg}};
            box-shadow: ${{props => props.theme.shadows.lg}};
        `;
        
        // Esporta i componenti e il tema
        window.BaseComponents = {{
            Button: BaseButton,
            Input: BaseInput,
            Container: BaseContainer
        }};
        
        window.theme = defaultTheme;
        """
    
    def _generate_root_component(self) -> str:
        """Genera il componente root con il provider del tema"""
        strict_mode = "React.StrictMode" if self.config.use_strict_mode else "React.Fragment"
        
        # Genera i dati del tema
        theme_data = {
            "colors": {k: v.to_hex() if hasattr(v, 'to_hex') else v 
                      for k, v in self._theme.tokens.colors.items()},
            "spacing": self._theme.tokens.spacing,
            "typography": self._theme.tokens.typography,
            "shadows": self._theme.tokens.shadows,
            "radii": self._theme.tokens.radii,
            "transitions": self._theme.tokens.transitions
        }
        
        return f"""
            <{strict_mode}>
                {{/* Passa i dati del tema come stringa JSON */}}
                <ThemeProvider theme={{...{json.dumps(theme_data)}}}>
                    <PythonProvider>
                        <App {{...props}} />
                    </PythonProvider>
                </ThemeProvider>
            </{strict_mode}>
        """
    
    def inject_api(self, api_object: Any) -> None:
        """Inietta un oggetto API nel contesto React"""
        if not self._window:
            logger.warning("Window not initialized. API injection delayed.")
            return
            
        # Espose tutti i metodi pubblici dell'oggetto API
        for method_name in dir(api_object):
            if not method_name.startswith('_'):  # Solo metodi pubblici
                method = getattr(api_object, method_name)
                if callable(method):
                    self.expose_method(method_name, method)
        
        # Inietta l'API nel contesto React
        js_code = """
        window.pythonApi = {
            ...window.pythonApi,
            ...Object.fromEntries(
                Object.entries(window.pywebview.api)
                .filter(([key]) => !key.startsWith('_'))
            )
        };
        
        // Aggiorna il bridge Python con i nuovi metodi
        const bridge = window.createPythonBridge();
        window.dispatchEvent(new CustomEvent('pythonApiUpdated', { detail: bridge }));
        """
        
        self.invoke_js(js_code)
        logger.debug(f"Injected API methods: {list(self._api_methods.keys())}")
    
    def _generate_styles(self) -> str:
        """Genera gli stili CSS globali"""
        return f"""
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: {self.config.font_family};
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                background: {self.config.background_color};
                color: {self._theme.tokens.colors.get("text", "#000000")};
                line-height: 1.5;
            }}
            
            #root {{
                width: 100%;
                height: 100vh;
                overflow: auto;
                display: flex;
                flex-direction: column;
            }}
            
            button {{
                cursor: pointer;
                border: none;
                outline: none;
                font-family: inherit;
            }}
            
            input, textarea {{
                font-family: inherit;
                outline: none;
            }}
            
            /* Animazioni di base */
            .fade-enter {{
                opacity: 0;
            }}
            
            .fade-enter-active {{
                opacity: 1;
                transition: opacity 200ms ease-in;
            }}
            
            .fade-exit {{
                opacity: 1;
            }}
            
            .fade-exit-active {{
                opacity: 0;
                transition: opacity 200ms ease-out;
            }}
            
            /* Utility classes */
            .flex {{ display: flex; }}
            .flex-col {{ flex-direction: column; }}
            .items-center {{ align-items: center; }}
            .justify-center {{ justify-content: center; }}
            .gap-1 {{ gap: 0.25rem; }}
            .gap-2 {{ gap: 0.5rem; }}
            .gap-4 {{ gap: 1rem; }}
        </style>
        """