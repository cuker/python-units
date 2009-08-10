"""Test conversion between units using the 'in' operator"""

from units import unit
import units.named_composed_unit
import units.composed_unit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

from py.test import raises

def test_valid_conversion_from_named_to_basic():
    """Named units should convert to their basic equivalents"""
    km = units.named_composed_unit.make('km',
                                        units.composed_unit.make([unit('m')],
                                                                 [],
                                                                 multiplier=1000),
                                        is_si=False)
    
    one_km_in_m = (Quantity(1, km) in unit('m'))
    
    assert one_km_in_m == Quantity(1000, unit('m'))
    assert one_km_in_m.unit == unit('m')
    
def test_valid_conversion_from_basic_to_named():
    """Named units should convert to their basic equivalents"""
    km = units.named_composed_unit.make('km',
                                        units.composed_unit.make([unit('m')],
                                                                 [],
                                                                 multiplier=1000),
                                        is_si=False)
    
    one_thousand_m_in_km = Quantity(1000, unit('m')) in km
    
    assert one_thousand_m_in_km == Quantity(1, km)
    assert one_thousand_m_in_km.unit == km