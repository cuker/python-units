"""SI units can take PREFIXES which imply a multiplier. The si module
encodes logic to handle these PREFIXES and create SI units."""

import units
import units.composed_unit
import units.named_composed_unit

PREFIXES = {
    'Y' : 10 ** 24,
    'Z' : 10 ** 21,
    'E' : 10 ** 18,
    'P' : 10 ** 15,
    'T' : 10 ** 12,
    'G' : 10 ** 9,
    'M' : 10 ** 6,
    'k' : 10 ** 3,
    'h' : 10 ** 2,
    'da' : 10 ** 1,
    'd' : 10 ** -1,
    'c' : 10 ** -2,
    'm' : 10 ** -3,
    'u' : 10 ** -6,
    'n' : 10 ** -9,
    'p' : 10 ** -12,
    'f' : 10 ** -15,
    'a' : 10 ** -18,
    'z' : 10 ** -21,
    'y' : 10 ** -24,
}


def prefixed(unit_str):
    """True iff the given string is prefixed by an SI prefix."""
    return ((unit_str[0:2] in PREFIXES and len(unit_str) > 2) or 
           (unit_str[0] in PREFIXES and len(unit_str) > 1))


def multiplier(unit_str):
    """The multiplier implied by the SI-prefixed given string."""
    assert(prefixed(unit_str))
    if unit_str[0:2] in PREFIXES:
        return PREFIXES[unit_str[0:2]]
    else:
        return PREFIXES[unit_str[0]]


def without_prefix(unit_str):
    """The non-prefixed version of the given SI-prefixed string."""
    assert(prefixed(unit_str))
    if unit_str[0:2] in PREFIXES:
        return unit_str[2:]
    else:
        return unit_str[1:]


def can_make(unit_str, registry=units.REGISTRY):
    """True if the given unit string represents an SI unit."""
    return prefixed(unit_str) and units.unit(without_prefix(unit_str), registry).si
        

def make(unit_str, registry=units.REGISTRY):
    """Create a unit object from the given SI-unit string."""
    assert can_make(unit_str)
    return units.named_composed_unit.make(unit_str,
            units.composed_unit.make([units.unit(without_prefix(unit_str))],
                [],
                multiplier(unit_str),
                registry),
            registry)