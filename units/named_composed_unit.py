"""Assign arbitrary new symbols to composed units."""

from units.abstract import AbstractUnit
from units.composed_unit import ComposedUnit
from units.registry import REGISTRY

class NamedComposedUnit(AbstractUnit):
    """A NamedComposedUnit is a composed unit with its own symbol."""
    
    def get_specifier(self):
        """The key for the composed unit"""
        return self._specifier
    specifier = property(get_specifier)
    
    def get_symbal(self):
        """The symbal for the composed unit"""
        return self._symbal
    symbal = property(get_symbal)
    
    def get_name(self):
        """The label for the composed unit"""
        return self._name
    name = property(get_name)
    
    def get_composed_unit(self):
        """The labeled composed unit"""
        return self._composed_unit
    composed_unit = property(get_composed_unit)
    
    def __new__(cls, specifier, composed_unit, symbal=u'', name=u'', is_si=False):
        """Give a composed unit a new symbol."""
        # pylint: disable-msg=W0613
        if specifier not in REGISTRY:
            REGISTRY[specifier] = super(NamedComposedUnit, cls).__new__(cls)
        return REGISTRY[specifier]
    
    def __init__(self, specifier, composed_unit, symbal=u'', name=u'', is_si=False):
        super(NamedComposedUnit, self).__init__(is_si)
        self._specifier = specifier
        self._composed_unit = composed_unit
        if symbal:
            self._symbal = symbal
        else:
            self._symbal = specifier
        self._name = name
    
    def invert(self):
        """Return the invert of the underlying composed unit."""
        return self.composed_unit.invert()
    
    def canonical(self):
        """Return the canonical of the underlying composed unit."""
        return self.composed_unit.canonical()
    
    def squeeze(self):
        """Return the squeeze of the underlying composed unit."""
        return self.composed_unit.squeeze()
    
    def __mul__(self, other):
        return ComposedUnit([self, other], [])
    
    def __div__(self, other):
        return ComposedUnit([self], [other])
    
    __str__ = get_name
    
    def __repr__(self):
        return '%(name)s(%(params)s)' % {
            'name': self.__class__.__name__,
            'params': ', '.join([repr(x) for x in [self.specifier, self.composed_unit, self.symbal, self.name, self.is_si()]])
        }
    
    def __eq__(self, other):
        return self.composed_unit == other or other == self.composed_unit
    
    def __pow__(self, exponent):
        return self.composed_unit ** exponent