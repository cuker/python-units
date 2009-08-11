"""Provides support for quantities and units, which strictly disallow
invalid operations between incompatible quantities. For example, we cannot add 
2 metres to 5 seconds, because this doesn't make sense.

@requires: U{Python<http://python.org/>} >= 2.5
@since: 2009-Aug-10
@status: under development
"""

__author__    = 'Aran Donohue'
__version__   = '0.00'
__copyright__ = '2009'
__license__   = 'Python Software Foundation License'
__contact__   = 'aran@arandonohue.com'

class Unit(object):
    """Factory for units."""
    
    Registry = {}
    
    def __new__(cls, unit_str, registry=Registry):
        """Create a unit object from a given string specification.

        >>> registry = {}
        >>> Unit('m', registry=registry) == Unit('m', registry=registry)
        True
        >>> Unit('m', registry=registry) != Unit('s', registry=registry)
        True
        """
        if unit_str in registry:
            return registry[unit_str]
        if units.si.can_make(unit_str, registry):
            return units.si.make(unit_str, registry)
        else:
            result = LeafUnit.__new__(LeafUnit, unit_str, False, registry)
            result.__init__(unit_str, False)
            return result


import units.si
from  units.leaf_unit import LeafUnit

    