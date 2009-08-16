"""Test conversion between units using the 'in' operator"""

from units import unit
from units.predefined import define_units
from units.quantity import Quantity
from units.registry import REGISTRY

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
        
    define_units()
    kilometre = unit('km')
    one_km_in_m = unit('m')(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, unit('m'))
    assert one_km_in_m.unit == unit('m')

def teardown_module(module):
    # Disable warning about not using module.
    # pylint: disable-msg=W0613
    """Called after running all of the tests here."""
    REGISTRY.clear()