from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import dataclass
import json
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = None

class MetricsCollector:
    def __init__(self, export_path: Optional[Path] = None):
        self._metrics: List[Metric] = []
        self._export_path = export_path
        
    def record(self, name: str, value: float, tags: Dict[str, str] = None):
        """Registra una metrica"""
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags
        )
        self._metrics.append(metric)
        
    def export(self):
        """Esporta le metriche"""
        if self._export_path:
            metrics_data = [
                {
                    "name": m.name,
                    "value": m.value,
                    "timestamp": m.timestamp,
                    "tags": m.tags
                }
                for m in self._metrics
            ]
            
            with open(self._export_path, 'w') as f:
                json.dump(metrics_data, f, indent=2) 