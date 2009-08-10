"""Assign arbitrary new symbols to composed units."""
from units import REGISTRY as GLOBAL_REGISTRY
from units.compatibility import compatible
from units.exception import IncompatibleUnitsException

def make(name, composed_unit, is_si=False):
    """Give a composed unit a new symbol."""

    if name not in GLOBAL_REGISTRY:
        GLOBAL_REGISTRY[name] = NamedComposedUnit(name, composed_unit, is_si)
    
    return GLOBAL_REGISTRY[name]

class NamedComposedUnit(object):
    """A NamedComposedUnit is a composed unit with its own symbol."""

    def get_name(self):
        """The label for the composed unit"""
        return self._name
    name = property(get_name)
    
    def get_composed_unit(self):
        """The labeled composed unit"""
        return self._composed_unit
    composed_unit = property(get_composed_unit)
    
    def get_si(self):
        """Whether this composed unit can accept SI prefixes"""
        return self._si
    si = property(get_si)

    def __init__(self, name, composed_unit, is_si):
        self._name = name
        self._composed_unit = composed_unit
        self._si = is_si

    def canonical(self):
        return self.composed_unit.canonical()
        
    def squeeze(self):
        return self.composed_unit.squeeze()
        
    def invert(self):
        return self.composed_unit.invert()
        
    def __mul__(self, other):
        return self.composed_unit * other
    def __div__(self, other):
        return self.composed_unit / other
        
    def __contains__(self, quantity):
        """Overload the 'in' operator to convert units."""
        if compatible(self, quantity.unit):
            return Quantity(quantity.num * quantity.unit.squeeze(), self)
        else:
            raise IncompatibleUnitsException()