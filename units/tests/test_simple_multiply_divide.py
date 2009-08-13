"""Tests of simple multiplication and division of units and quantities."""

from units import Unit
from units.quantity import Quantity

def test_simple_multiply():
    """Simple multiplication of units."""
    assert Unit('m') * Unit('s') / Unit('s') == Unit('m')

def test_simple_divide():
    """Simple division of units."""
    assert Unit('m') / Unit('s') * Unit('s') == Unit('m')

def test_commutative_multiply():
    """Commutative multiplication of units"""
    
    assert Unit('m') * Unit('s') / Unit('m') == Unit('s')

def test_simple_multiply_quantity():
    """Simple multiplication of quantities"""
    assert (Quantity(2, Unit('m')) * 
            Quantity(2, Unit('s')) ==
            Quantity(4, Unit('m') * Unit('s')))
            
    assert (Quantity(2, Unit('s')) * 
            Quantity(2, Unit('m')) ==
            Quantity(4, Unit('m') * Unit('s')))

def test_simple_divide_quantity():
    """Simple division of quantities"""
    assert (Quantity(8, Unit('m')) / 
            Quantity(2, Unit('s')) ==
            Quantity(4, Unit('m') / Unit('s')))

Unit.Registry.clear()
assert len(Unit.Registry) == 0