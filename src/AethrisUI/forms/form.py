from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from ..hooks import use_state, use_effect

@dataclass
class ValidationRule:
    check: Callable[[Any], bool]
    message: str

class FormField:
    def __init__(self, initial_value: Any = None, validators: List[ValidationRule] = None):
        self.value = initial_value
        self.validators = validators or []
        self.errors: List[str] = []
    
    def validate(self) -> bool:
        self.errors = []
        for rule in self.validators:
            if not rule.check(self.value):
                self.errors.append(rule.message)
        return len(self.errors) == 0

def use_form(initial_values: Dict[str, Any], validators: Dict[str, List[ValidationRule]] = None):
    form_data, set_form_data = use_state(initial_values)
    errors, set_errors = use_state({})
    
    def set_field(field: str, value: Any):
        new_data = {**form_data, field: value}
        set_form_data(new_data)
        
        if validators and field in validators:
            field_errors = []
            for rule in validators[field]:
                if not rule.check(value):
                    field_errors.append(rule.message)
            set_errors({**errors, field: field_errors})
    
    def submit(on_submit: Callable[[Dict[str, Any]], None]):
        is_valid = True
        new_errors = {}
        
        if validators:
            for field, rules in validators.items():
                field_errors = []
                for rule in rules:
                    if not rule.check(form_data.get(field)):
                        field_errors.append(rule.message)
                if field_errors:
                    is_valid = False
                    new_errors[field] = field_errors
        
        set_errors(new_errors)
        if is_valid:
            on_submit(form_data)
    
    return form_data, set_field, errors, submit 