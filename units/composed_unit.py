"""Composed units are quotients of products of other units 
(but not other composed units.) 
Utility methods here for working with abstract fractions."""

from units import REGISTRY
from units.compatibility import compatible


def make(numer, denom, multiplier=1):
    """Construct a unit that is a quotient of products of units, 
    including an implicit quantity multiplier."""
    (mult, simple_numer, simple_denom) = cancel(numer, denom)
    
    multiplier *= mult
    
    wrung_mult, wrung_numer = wring(simple_numer)
    wrung_div, wrung_denom = wring(simple_denom)
    
    multiplier *= wrung_mult / wrung_div
    
    wrung_numer.sort()
    wrung_denom.sort()
            
    if not wrung_denom:
        if len(wrung_numer) == 1:
            if multiplier == 1:
                return wrung_numer[0]
            else:
                pass
        elif not wrung_numer:
            return multiplier
        else:
            pass
    else:
        pass
            
    key = (multiplier, tuple(wrung_numer), tuple(wrung_denom))
    if key not in REGISTRY:
        REGISTRY[key] = ComposedUnit(wrung_numer, wrung_denom, multiplier)
    return REGISTRY[key]

def cancel(numer, denom):
    """Cancel out compatible units in the given numerator and denominator.
    Return a triple of the implied quantity multiplier that has been 
    squeezed out, the new numerator and the new denominator."""
    multiplier = 1
    
    simple_numer = numer[:]
    simple_denom = denom[:]
    
    for nleaf in simple_numer:
        for dleaf in simple_denom:
            if compatible(nleaf, dleaf):
                multiplier *= nleaf.squeeze() / dleaf.squeeze()
                simple_numer.remove(nleaf)
                simple_denom.remove(dleaf)
                
    return (multiplier, simple_numer, simple_denom)
    
def wring(lst):
    """Reduce each unit in lst to its canonical form.
    Return a tuple of the combined quantity multiplier from the units 
    and the new units."""
    multiplier = 1
    result = []
    for unit in lst:
        multiplier *= unit.squeeze()
        result.append(unit.canonical())
        
    return (multiplier, result)

class ComposedUnit(object):
    """A ComposedUnit is a quotient of products of units."""
    def __init__(self, numer, denom, multiplier):
        self.numer = numer
        self.denom = denom
        self.multiplier = multiplier        
    
    si = property(lambda self: False)
             
    def __repr__(self):
        # Not a call to 'make' because we've thrown away the creating units.
        # Because it circumvents the factory, the below repr shouldn't actually 
        # be used, so we surround it with <> to make sure that's clear
        return ("<ComposedUnit(" + 
                ', '.join([repr(x) for x in [self.numer, 
                                             self.denom,
                                             self.multiplier]]) + ")>")
        
    def __str__(self):
        if self.denom:
            return (('*'.join([str(x) for x in self.numer]) or '1') + " / "
                    + '*'.join([str(x) for x in self.denom]))
        else:
            return '*'.join([str(x) for x in self.numer])
            
    def canonical(self):
        """Return an immutable, comparable version of this unit."""
        return (tuple(self.numer), tuple(self.denom))
        
    def squeeze(self):
        """Return this unit's implicit quantity multiplier."""
        return self.multiplier
        
    def __mul__(self, other):
        if hasattr(other, "numer"):
            assert(hasattr(other, "denom"))
            return make(self.numer + other.numer, 
                        self.denom + other.denom, 
                        self.squeeze() * other.squeeze())
        else:
            return make(self.numer + [other], 
                        self.denom, 
                        self.squeeze() * other.squeeze())
            
    def invert(self):
        """Return (this unit)^-1."""
        return make(self.denom, self.numer, 1 / self.squeeze())
        
    def __div__(self, other):
        if hasattr(other, "invert"):
            return self * other.invert()
        else:
            return make(self.numer, 
                        self.denom + [other], 
                        self.squeeze() / other.squeeze())
            