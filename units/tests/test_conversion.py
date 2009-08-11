"""Test conversion between units using the 'in' operator"""

from units import unit
import units.named_composed_unit
import units.composed_unit
from units.quantity import Quantity

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
    
    registry = {}
    
    kilometre = units.named_composed_unit.make(
        'km',
        units.composed_unit.make([unit('m', registry=registry)],
                                 [],
                                 multiplier=1000,
                                 registry=registry),
        registry=registry)
    
    one_km_in_m = unit('m', registry=registry)(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, unit('m', registry=registry))
    assert one_km_in_m.unit == unit('m', registry=registry)
    
#def test_valid_basic_to_named():
#    """Named units should convert to their basic equivalents"""
#    
#    registry = {}
#    
#    kilometre = units.named_composed_unit.make(
#                    'km',
#                    units.composed_unit.make([unit('m', registry=registry)],
#                                             [],
#                                             multiplier=1000,
#                                             registry=registry),
#                    registry=registry)
#    
#    one_thousand_m_in_km = kilometre(Quantity(1000, 
#                                              unit('m', registry=registry)))
#    
#    assert one_thousand_m_in_km == Quantity(1, kilometre)
#    assert one_thousand_m_in_km.unit == kilometre