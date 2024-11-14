from typing import Dict, Any, Optional, List
import json
import logging
import time
from pathlib import Path

class DebugInfo:
    def __init__(self):
        self.component_tree: Dict[str, Any] = {}
        self.style_computations: Dict[str, Any] = {}
        self.event_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {}
    
    def export(self, path: Path):
        with open(path, 'w') as f:
            json.dump({
                "component_tree": self.component_tree,
                "style_computations": self.style_computations,
                "event_history": self.event_history,
                "performance_metrics": self.performance_metrics
            }, f, indent=2)

class DebugRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.debug_info = DebugInfo()
        
    def render(self, node):
        # Cattura informazioni di debug prima del rendering
        self.debug_info.component_tree = self._capture_tree(node)
        
        # Esegui il rendering
        start_time = time.perf_counter()
        result = self.renderer.render(node)
        end_time = time.perf_counter()
        
        # Salva metriche di performance
        self.debug_info.performance_metrics["render_time"] = end_time - start_time
        
        return result