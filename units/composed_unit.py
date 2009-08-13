"""Composed units are quotients of products of other units 
(but not other composed units.) 
Utility methods here for working with abstract fractions."""

import units
from units.compatibility import compatible

def collapse(numer, denom, multiplier):
    """Attempts to convert the fractional unit represented by the parameters
    into another, simpler type. Returns the simpler unit or None if no 
    simplification is possible.
    """
    
    if not denom and not numer:
        return multiplier

    if not denom and len(numer) == 1 and multiplier == 1:
        return numer[0]
        
    return None

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
    
def squeeze(numer, denom, multiplier):
    """Return this unit's implicit quantity multiplier.
    
    Some units imply quantities. For example, a kilometre implies a quantity
    of a thousand metres. This 'squeezes' out these implied quantities, 
    returning a modified multiplier and simpler units."""
    (mult, simple_numer, simple_denom) = cancel(numer, denom)

    multiplier *= mult
    
    wrung_mult, wrung_numer = wring(simple_numer)
    wrung_div, wrung_denom = wring(simple_denom)
    
    multiplier *= wrung_mult / wrung_div
    
    wrung_numer.sort()
    wrung_denom.sort()
    
    return (wrung_numer, wrung_denom, multiplier)

class ComposedUnit(object):
    """A ComposedUnit is a quotient of products of units."""
    
    def __new__(cls, numer, denom, multiplier=1, registry=units.Unit.Registry):
        """Construct a unit that is a quotient of products of units, 
        including an implicit quantity multiplier."""
       
        (wrung_numer, wrung_denom, wrung_multiplier) = squeeze(numer, 
                                                               denom, 
                                                               multiplier)

        simpler = collapse(wrung_numer, wrung_denom, multiplier)
        if simpler:
            return simpler

        key = (multiplier, tuple(wrung_numer), tuple(wrung_denom))
        if key not in registry:
            registry[key] = super(ComposedUnit, cls).__new__(cls)
        return registry[key]
    
    def __init__(self, numer, denom, multiplier=1, registry=None):
        (self.numer, self.denom, self.multiplier) = squeeze(numer, 
                                                            denom, 
                                                            multiplier)        
    
    si = property(lambda self: False)
             
    def __str__(self):
        if self.denom:
            return (('*'.join([str(x) for x in self.numer]) or '1') + " / "
                    + '*'.join([str(x) for x in self.denom]))
        else:
            return '*'.join([str(x) for x in self.numer])
    __repr__ = __str__
            
    def canonical(self):
        """Return an immutable, comparable version of this unit."""
        if self.denom or len(self.numer) != 1:
            return (tuple(self.numer), tuple(self.denom))
        else:
            return self.numer[0]
        
    def squeeze(self):
        """Return this unit's implicit quantity multiplier."""
        return self.multiplier
        
    def __mul__(self, other):
        if hasattr(other, "numer"):
            assert(hasattr(other, "denom"))
            return ComposedUnit(self.numer + other.numer, 
                                self.denom + other.denom, 
                                self.squeeze() * other.squeeze())
        else:
            return ComposedUnit(self.numer + [other], 
                                self.denom, 
                                self.squeeze() * other.squeeze())
            
    def invert(self):
        """Return (this unit)^-1."""
        return ComposedUnit(self.denom, self.numer, 1 / self.squeeze())
        
    def __div__(self, other):
        if hasattr(other, "invert"):
            return self * other.invert()
        else:
            return ComposedUnit(self.numer, 
                                self.denom + [other], 
                                self.squeeze() / other.squeeze())
            