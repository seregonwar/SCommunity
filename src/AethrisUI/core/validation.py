from typing import Dict, Any, Type, Callable, Optional, List
from dataclasses import dataclass

@dataclass
class PropValidator:
    type: Type
    required: bool = False
    validator: Optional[Callable[[Any], bool]] = None
    error_message: str = ""

class ComponentValidator:
    def __init__(self):
        self.prop_validators: Dict[str, PropValidator] = {}
        
    def add_validator(self, prop_name: str, validator: PropValidator):
        self.prop_validators[prop_name] = validator
        
    def validate(self, props: Dict[str, Any]) -> List[str]:
        errors = []
        
        for name, validator in self.prop_validators.items():
            if name not in props and validator.required:
                errors.append(f"Missing required prop: {name}")
                continue
                
            if name in props:
                value = props[name]
                if not isinstance(value, validator.type):
                    errors.append(f"Invalid type for {name}: expected {validator.type.__name__}")
                
                if validator.validator and not validator.validator(value):
                    errors.append(validator.error_message or f"Validation failed for {name}")
        
        return errors 