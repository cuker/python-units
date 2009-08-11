"""Leaf units stand alone. 
They are not compatible with any other kind of unit."""

import units
from units.compatibility import compatible
from units.exception import IncompatibleUnitsException
from units.quantity import Quantity
import units.composed_unit


def make(symbol, is_si, registry=units.REGISTRY):
    """Make a new LeafUnit with the given unit symbol and SI-compatibility.
    A unit that is SI compatible can be prefixed e.g. with k to mean 1000x.
    
    >> make('m', is_si=True)
    units.leaf_unit.make('m', True)
    >> make('mi', is_si=False)
    units.leaf_unit.make('mi', False)
    
    """
    if symbol not in registry:
        registry[symbol] = LeafUnit(symbol, is_si)

    return registry[symbol]
    
class LeafUnit(object):
    """Leaf units are not compatible with other units, but they can be 
    composed to make other units."""
    
    def is_si(self):
        """True if the unit can take SI prefixes."""
        return self._si
    si = property(is_si)
    
    def get_unit_str(self):
        """Return the symbol of the unit."""
        return self._unit_str
    unit_str = property(get_unit_str)
        
    def __init__(self, unit_str, is_si):
        self._unit_str = unit_str.strip()
        self._si = is_si
              
    __str__ = get_unit_str
    __repr__ = __str__
    
    def __mul__(self, other):
        if hasattr(other, "numer"):
            return other * self
        
        else:
            return units.composed_unit.make([self, other], [])
    
    def __div__(self, other):
        if hasattr(other, "invert"):
            return other.invert() * self
        else:
            return units.composed_unit.make([self], [other])
    
    def invert(self):
        """Return (this unit)^-1"""
        return units.composed_unit.make([], [self])
    
    def canonical(self):
        """A LeafUnit is its own canonical form."""
        return self
        
    squeeze = lambda self: 1
    
    def __contains__(self, quantity):
        """Overload the 'in' operator to convert units."""
        if compatible(self, quantity.unit):
            return Quantity(quantity.num * quantity.unit.squeeze(), self)
        else:
            raise IncompatibleUnitsException()