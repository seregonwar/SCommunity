from dataclasses import dataclass
from typing import Union, List
import re

@dataclass
class Unit:
    value: float
    unit: str
    
    def __str__(self):
        return f"{self.value}{self.unit}"

class Px(Unit):
    def __init__(self, value: float):
        super().__init__(value, "px")

class Rem(Unit):
    def __init__(self, value: float):
        super().__init__(value, "rem")

def parse_calc(value: str) -> int:
    """Parsa una funzione calc() e restituisce il valore calcolato"""
    # Rimuovi calc() e spazi
    expr = value.replace('calc(', '').replace(')', '').strip()
    
    # Per ora gestiamo solo operazioni semplici
    if '-' in expr:
        parts = expr.split('-')
        return parse_unit(parts[0]) - parse_unit(parts[1])
    elif '+' in expr:
        parts = expr.split('+')
        return parse_unit(parts[0]) + parse_unit(parts[1])
    elif '*' in expr:
        parts = expr.split('*')
        return parse_unit(parts[0]) * parse_unit(parts[1])
    elif '/' in expr:
        parts = expr.split('/')
        return parse_unit(parts[0]) // parse_unit(parts[1])
    
    return parse_unit(expr)

def parse_unit(value: Union[str, int, float]) -> int:
    """Converte un valore di dimensione in pixel"""
    if isinstance(value, (int, float)):
        return int(value)
    
    if isinstance(value, str):
        value = value.strip().lower()
        
        # Gestisci calc()
        if value.startswith('calc('):
            return parse_calc(value)
        
        # Gestisci valori singoli
        if ' ' in value:
            value = value.split()[0]
            
        if value.endswith('px'):
            return int(float(value[:-2]))
        if value.endswith('%'):
            # Per ora trattiamo le percentuali come pixel
            return int(float(value[:-1]))
        if value.endswith('rem'):
            # Assumiamo 1rem = 16px
            return int(float(value[:-3]) * 16)
        try:
            return int(float(value))
        except ValueError:
            return 0
    return 0

def parse_multiple_units(value: str) -> List[int]:
    """Converte una stringa con più valori di dimensione in una lista di pixel"""
    if not value:
        return [0]
        
    parts = value.strip().split()
    return [parse_unit(part) for part in parts]

def parse_padding(value: Union[str, int, float]) -> int:
    """Converte un valore di padding in pixel, usando il primo valore se ce ne sono multipli"""
    if isinstance(value, str) and ' ' in value:
        return parse_multiple_units(value)[0]
    return parse_unit(value)