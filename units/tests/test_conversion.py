"""Test conversion between units using the 'in' operator"""

from units import unit
import units.named_composed_unit
import units.composed_unit
from units.quantity import Quantity

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
    kilometre = units.named_composed_unit.make(
        'km',
        units.composed_unit.make([unit('m')],
                                 [],
                                 multiplier=1000))
    
    one_km_in_m = (Quantity(1, kilometre) in unit('m'))
    
    assert one_km_in_m == Quantity(1000, unit('m'))
    assert one_km_in_m.unit == unit('m')
    
def test_valid_basic_to_named():
    """Named units should convert to their basic equivalents"""
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m')],
                                             [],
                                             multiplier=1000))
    
    one_thousand_m_in_km = Quantity(1000, unit('m')) in kilometre
    
    assert one_thousand_m_in_km == Quantity(1, kilometre)
    assert one_thousand_m_in_km.unit == kilometre