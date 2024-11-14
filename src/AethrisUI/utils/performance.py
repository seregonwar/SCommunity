from typing import Dict, Any
import time
import cProfile
import pstats
from functools import wraps

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.profiler = cProfile.Profile()
    
    def start_profiling(self):
        self.profiler.enable()
    
    def stop_profiling(self):
        self.profiler.disable()
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        return stats
    
    def measure_time(self, name: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                
                if name not in self.metrics:
                    self.metrics[name] = []
                self.metrics[name].append(end - start)
                
                return result
            return wrapper
        return decorator 