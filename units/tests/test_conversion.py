"""Test conversion between units using the 'in' operator"""

from units import Unit
from units.predefined import define_units
from units.quantity import Quantity
from units.registry import REGISTRY

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
        
    define_units()
    kilometre = Unit('km')
    one_km_in_m = Unit('m')(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, Unit('m'))
    assert one_km_in_m.unit == Unit('m')

REGISTRY.clear()
