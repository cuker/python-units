"""SI units can take PREFIXES which imply a multiplier. The si module
encodes logic to handle these PREFIXES and create SI units."""

from __init__ import scaled_unit
from units.registry import REGISTRY

PREFIXES = {
    'Y' : {'prefix': 'yotta', 'multiplier': 10 ** 24},
    'Z' : {'prefix': 'zetta', 'multiplier': 10 ** 21},
    'E' : {'prefix': 'exa', 'multiplier': 10 ** 18},
    'P' : {'prefix': 'peta', 'multiplier': 10 ** 15},
    'T' : {'prefix': 'tera', 'multiplier': 10 ** 12},
    'G' : {'prefix': 'giga', 'multiplier': 10 ** 9},
    'M' : {'prefix': 'mega', 'multiplier': 10 ** 6},
    'k' : {'prefix': 'kilo', 'multiplier': 10 ** 3},
    'h' : {'prefix': 'hecto', 'multiplier': 10 ** 2},
    'da' : {'prefix': 'deca', 'multiplier': 10 ** 1},
    'd' : {'prefix': 'deci', 'multiplier': 10 ** -1},
    'c' : {'prefix': 'centi', 'multiplier': 10 ** -2},
    'm' : {'prefix': 'milli', 'multiplier': 10 ** -3},
    'u' : {'prefix': 'micro', 'multiplier': 10 ** -6},
    'n' : {'prefix': 'nano', 'multiplier': 10 ** -9},
    'p' : {'prefix': 'pico', 'multiplier': 10 ** -12},
    'f' : {'prefix': 'femto', 'multiplier': 10 ** -15},
    'a' : {'prefix': 'atto', 'multiplier': 10 ** -18},
    'z' : {'prefix': 'zepto', 'multiplier': 10 ** -21},
    'y' : {'prefix': 'yocto', 'multiplier': 10 ** -24},
}


def prefixed(unit_str):
    """True if the given string is prefixed by an SI prefix."""
    return ((unit_str[0:2] in PREFIXES and len(unit_str) > 2) or (unit_str[0] in PREFIXES and len(unit_str) > 1))

def without_prefix(unit_str):
    """The non-prefixed version of the given SI-prefixed string."""
    assert prefixed(unit_str)
    if unit_str[0:2] in PREFIXES:
        return unit_str[2:]
    else:
        return unit_str[1:]

def can_make(unit_str):
    """True if the given unit string represents an SI unit."""
    if prefixed(unit_str):
        unit = REGISTRY.get(without_prefix(unit_str), None)
        if unit:
            return unit.is_si()
    return False

def prefixed_unit(unit_str):
    """Create a unit object from the given SI-unit string."""
    base_unit = REGISTRY[without_prefix(unit_str)]
    
    if unit_str[0:2] in PREFIXES:
        prefix = PREFIXES[unit_str[0:2]]
    else:
        prefix = PREFIXES[unit_str[0]]
        
    return scaled_unit(unit_str, base_unit.name, multiplier=prefix['multiplier'], name='%s%s' % (prefix['prefix'], base_unit.name))