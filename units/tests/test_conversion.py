"""Test conversion between units using the 'in' operator"""

from units import Unit
from units.named_composed_unit import NamedComposedUnit
from units.composed_unit import ComposedUnit
from units.quantity import Quantity

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
        
    kilometre = NamedComposedUnit(
        'km',
        ComposedUnit([Unit('m')],
                     [],
                     multiplier=1000))
    
    one_km_in_m = Unit('m')(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, Unit('m'))
    assert one_km_in_m.unit == Unit('m')

Unit.Registry.clear()
assert len(Unit.Registry) == 0