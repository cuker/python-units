"""Test conversion between units using the 'in' operator"""

from units import unit
import units.named_composed_unit
import units.composed_unit
from units.quantity import Quantity

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
    
    r = {}
    
    kilometre = units.named_composed_unit.make(
        'km',
        units.composed_unit.make([unit('m', registry=r)],
                                 [],
                                 multiplier=1000,
                                 registry=r),
        registry=r)
    
    one_km_in_m = unit('m', registry=r)(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, unit('m', registry=r))
    assert one_km_in_m.unit == unit('m', registry=r)
    
def test_valid_basic_to_named():
    """Named units should convert to their basic equivalents"""
    
    r = {}
    
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m', registry=r)],
                                             [],
                                             multiplier=1000,
                                             registry=r),
                    registry=r)
    
    one_thousand_m_in_km = kilometre(Quantity(1000, unit('m', registry=r)))
    
    assert one_thousand_m_in_km == Quantity(1, kilometre)
    assert one_thousand_m_in_km.unit == kilometre