"""Provides support for quantities and units, which strictly disallow
invalid operations between incompatible quantities. For example, we cannot add 
2 metres to 5 seconds, because this doesn't make sense.

@requires: U{Python<http://python.org/>} >= 2.5
@since: 2009-Aug-10
@status: under development
"""

__author__    = 'Aran Donohue'
__version__   = '0.01'
__copyright__ = '2009'
__license__   = 'Python Software Foundation License'
__contact__   = 'aran@arandonohue.com'

import units.si
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units.registry import REGISTRY

def unit(specifier):
    """Main factory for units.
    
    >>> unit('m') == unit('m')
    True
    >>> unit('m') != unit('s')
    True
    """
    if specifier in REGISTRY:
        return REGISTRY[specifier]
    if units.si.can_make(specifier):
        return si_prefixed_unit(specifier)
    else:
        return LeafUnit(specifier, is_si=False)

def named_unit(symbol, 
         numer, 
         denom, 
         multiplier=1, 
         is_si=True):
    """Shortcut to create and return a new named unit."""
    
    numer_units = [unit(x) for x in numer]
    denom_units = [unit(x) for x in denom]
    
    return NamedComposedUnit(symbol,
            ComposedUnit(numer_units, 
                         denom_units,
                         multiplier), 
            is_si)

def scaled_unit(new_symbol, base_symbol, multiplier, is_si=False):
    """Shortcut to create and return a new unit that is 
    a scaled_unit multiplication of another."""
    return NamedComposedUnit(new_symbol, 
                             ComposedUnit([unit(base_symbol)], 
                                          [], 
                                          multiplier), 
                             is_si)

def si_prefixed_unit(unit_str):
    """Create a unit object from the given SI-unit string."""
    assert units.si.can_make(unit_str)
    return scaled_unit(unit_str, 
                  units.si.without_prefix(unit_str), 
                  units.si.multiplier(unit_str))

