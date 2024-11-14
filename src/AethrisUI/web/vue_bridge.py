from typing import Dict, Any, Optional
from .bridge_core import WebBridge, WebConfig

class VueBridge(WebBridge):
    def __init__(self, config: Optional[WebConfig] = None):
        super().__init__(config)
        
    def create_component(self, code: str, props: Optional[Dict[str, Any]] = None):
        html = self._generate_html(code, props)
        self.load_html(html)
        
    def _generate_html(self, code: str, props: Optional[Dict[str, Any]] = None) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
            <style>
                {self._get_default_styles()}
            </style>
        </head>
        <body>
            <div id="app"></div>
            <script>
                {self._get_bridge_api()}
                {code}
                
                const app = Vue.createApp({{
                    template: `<App/>`,
                    setup() {{
                        const python = Vue.inject('python');
                        return {{ python }};
                    }}
                }});
                
                app.component('App', App);
                app.provide('python', pythonBridge);
                app.mount('#app');
            </script>
        </body>
        </html>
        """
        
    def _get_bridge_api(self) -> str:
        return """
        const pythonBridge = {
            async invoke(method, ...args) {
                try {
                    const result = await window.pywebview.api.invoke(method, ...args);
                    return JSON.parse(result);
                } catch (error) {
                    console.error('Error invoking Python method:', error);
                    throw error;
                }
            },
            
            on(event, callback) {
                window.addEventListener(event, (e) => callback(e.detail));
            },
            
            emit(event, data) {
                window.pywebview.api.emit(event, JSON.stringify(data));
            }
        };
        """