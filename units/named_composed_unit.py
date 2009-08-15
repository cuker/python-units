"""Assign arbitrary new symbols to composed units."""
from units.registry import REGISTRY
from units.compatibility import compatible
from units.exception import IncompatibleUnitsException
from units.quantity import Quantity

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

    def __new__(cls, 
                name, 
                composed_unit, 
                is_si=False):
        """Give a composed unit a new symbol."""

        if name not in REGISTRY:
            REGISTRY[name] = super(NamedComposedUnit, 
                                   cls).__new__(cls)

        return REGISTRY[name]
        
    def __init__(self, name, composed_unit, is_si=False):
        self._name = name
        self._composed_unit = composed_unit
        self._si = is_si

    def __getattr__(self, name):
        return getattr(self.composed_unit, name)
        
    def __mul__(self, other):
        return self.composed_unit * other
    def __div__(self, other):
        return self.composed_unit / other
        
    __str__ = get_name

    def __repr__(self):
        return ("NamedComposedUnit(" + 
                ", ".join([repr(x) for x in [self.name, 
                                             self.composed_unit,
                                             self.si]])+
                ")")

    def __call__(self, quantity):
        """Overload the function call operator to convert units."""
        if compatible(self, quantity.unit):
            return Quantity(quantity.num * quantity.unit.squeeze(), self)
        else:
            raise IncompatibleUnitsException()
            
    def __eq__(self, other):
        return self.composed_unit == other or other == self.composed_unit
        
    def __pow__(self, exponent):
        return self.composed_unit ** exponent