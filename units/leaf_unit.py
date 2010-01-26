"""Leaf units stand alone.
They are not compatible with any other kind of unit."""

from units.abstract import AbstractUnit
from units.registry import REGISTRY
from units.composed_unit import ComposedUnit

class LeafUnit(AbstractUnit):
    """Leaf units are not compatible with other units, but they can be
    composed to make other units."""
    
    def get_specifier(self):
        """Return the symbol of the unit."""
        return self._specifier
    specifier = property(get_specifier)
    
    def get_symbal(self):
        return self._symbal
    symbal = property(get_symbal)
    
    def get_name(self):
        """Return the name of the unit."""
        return self._name
    name = property(get_name)
    
    def __new__(cls, specifier, symbal=u'', name=u'', is_si=False):
        # pylint: disable-msg=W0613
        if specifier not in REGISTRY:
            REGISTRY[specifier] = super(LeafUnit, cls).__new__(cls)
        return REGISTRY[specifier]
    
    def __init__(self, specifier, symbal=u'', name=u'', is_si=False):
        """Make a new LeafUnit with the given unit specifier and
        SI-compatibility. A unit that is SI compatible can be prefixed,
        e.g. with k to mean 1000x.
        """
        super(LeafUnit, self).__init__(is_si)
        
        self._specifier = specifier
        if symbal:
            self._symbal = symbal
        else:
            self._symbal = specifier
        self._name = name
    
    __str__ = get_specifier
    
    def __repr__(self):
        return '%(name)s(%(params)s)' % {
            'name': self.__class__.__name__,
            'params': ', '.join([repr(x) for x in [self.specifier, self.symbal, self.name, self.is_si()]])
        }
    
    def __mul__(self, other):
        if hasattr(other, "numer"):
            return other * self
        else:
            return ComposedUnit([self, other], [])
    
    def __div__(self, other):
        if hasattr(other, "invert"):
            return other.invert() * self
        else:
            return ComposedUnit([self], [other])
    
    def invert(self):
        """Return (this unit)^-1"""
        return ComposedUnit([], [self])
    
    def canonical(self):
        """A LeafUnit is its own canonical form."""
        return self
    
    def squeeze(self):
        """A LeafUnit has no implicit quantity."""
        return 1
    
    def __pow__(self, exponent):
        return ComposedUnit([self] * exponent, [], 1)