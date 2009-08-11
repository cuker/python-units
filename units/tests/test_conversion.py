"""Test conversion between units using the 'in' operator"""

from units import Unit
from units.named_composed_unit import NamedComposedUnit
from units.composed_unit import ComposedUnit
from units.quantity import Quantity

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
    
    registry = {}
    
    kilometre = NamedComposedUnit(
        'km',
        ComposedUnit([Unit('m', registry=registry)],
                                 [],
                                 multiplier=1000,
                                 registry=registry),
        registry=registry)
    
    one_km_in_m = Unit('m', registry=registry)(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, Unit('m', registry=registry))
    assert one_km_in_m.unit == Unit('m', registry=registry)
    
#def test_valid_basic_to_named():
#    """Named units should convert to their basic equivalents"""
#    
#    registry = {}
#    
#    kilometre = NamedComposedUnit(
#                    'km',
#                    ComposedUnit([Unit('m', registry=registry)],
#                                             [],
#                                             multiplier=1000,
#                                             registry=registry),
#                    registry=registry)
#    
#    one_thousand_m_in_km = kilometre(Quantity(1000, 
#                                              Unit('m', registry=registry)))
#    
#    assert one_thousand_m_in_km == Quantity(1, kilometre)
#    assert one_thousand_m_in_km.unit == kilometre