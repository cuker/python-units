"""Tests of simple multiplication and division of units and quantities."""

from units import unit
from units.quantity import Quantity

def test_simple_multiply():
    """Simple multiplication of units."""
    assert unit('m') * unit('s') / unit('s') == unit('m')

def test_simple_divide():
    """Simple division of units."""
    assert unit('m') / unit('s') * unit('s') == unit('m')

def test_commutative_multiply():
    """Commutative multiplication of units"""
    
    assert unit('m') * unit('s') / unit('m') == unit('s')

def test_simple_multiply_quantity():
    """Simple multiplication of quantities"""
    assert Quantity(4, unit('m') * unit('s')) == Quantity(2, unit('m')) * Quantity(2, unit('s'))
    assert Quantity(4, unit('m') * unit('s')) == Quantity(2, unit('s')) * Quantity(2, unit('m'))

def test_simple_divide_quantity():
    """Simple division of quantities"""
    assert Quantity(4, unit('m') / unit('s')) == Quantity(8, unit('m')) / Quantity(2, unit('s'))
