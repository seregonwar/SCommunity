from typing import Dict, List, Type
import time
from dataclasses import dataclass
from ..core import VirtualNode

@dataclass
class RenderMetrics:
    component_name: str
    render_time: float
    children_count: int
    props_count: int

class Profiler:
    _metrics: List[RenderMetrics] = []
    
    @classmethod
    def start_profiling(cls, component_name: str) -> float:
        return time.time()
    
    @classmethod
    def end_profiling(cls, start_time: float, component: VirtualNode):
        end_time = time.time()
        metrics = RenderMetrics(
            component_name=component.component_type,
            render_time=end_time - start_time,
            children_count=len(component.children),
            props_count=len(component.props)
        )
        cls._metrics.append(metrics)
    
    @classmethod
    def get_metrics(cls) -> List[RenderMetrics]:
        return cls._metrics

def profile_component(component_class: Type) -> Type:
    original_render = component_class.render
    
    def profiled_render(self) -> VirtualNode:
        start_time = Profiler.start_profiling(component_class.__name__)
        result = original_render(self)
        Profiler.end_profiling(start_time, result)
        return result
    
    component_class.render = profiled_render
    return component_class 