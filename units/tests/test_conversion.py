"""Test conversion between units using the 'in' operator"""

from units import unit
from units.compatibility import within_epsilon
from units.predefined import define_units
from units.quantity import Quantity
from units.registry import REGISTRY

def test_valid_named_to_basic():
    """Named units should convert to their basic equivalents"""
        
    kilometre = unit('km')
    one_km_in_m = unit('m')(Quantity(1, kilometre))
    
    assert one_km_in_m == Quantity(1000, unit('m'))
    assert one_km_in_m.unit == unit('m')
    assert str(one_km_in_m) == '1000 m'
    
def test_valid_basic_to_named():
    """Basic units should convert into named equivalents."""
    metre = unit('m')
    thousand_m_in_km = unit('km')(Quantity(1000, metre))
    
    assert thousand_m_in_km == Quantity(1, unit('km'))
    assert thousand_m_in_km.unit == unit('km')
    assert str(thousand_m_in_km) == '1 km'
    
def test_valid_composed_to_composed():
    """Valid composed units in terms of others."""
    metric_vel = unit('km') / unit('h')
    imp_vel = unit('mi') / unit('h')
    
    highway_kph = Quantity(100, metric_vel)
    highway_mph = Quantity(62.1371192237334, imp_vel)
    
    assert str(highway_kph) == '100 km / h'
    assert str(highway_mph) == '62.1371192237 mi / h'
    
    
    assert within_epsilon(imp_vel(highway_kph), 
                          highway_mph)

    assert str(imp_vel(highway_kph)) == '62.1371192237 mi / h'
    
    
def setup_module(module):
    # Disable warning about not using module.
    # pylint: disable-msg=W0613
    """Called by py.test before running any of the tests here."""
    define_units()

def teardown_module(module):
    # Disable warning about not using module.
    # pylint: disable-msg=W0613
    """Called after running all of the tests here."""
    REGISTRY.clear()