"""Tests for the Python built-in functions when applied
to Quantities.
"""

from units.predefined import define_units
from units.quantity import Quantity
from units.registry import REGISTRY
from units import Unit

def test_abs():
    """Absolute value of a quantity is a positive quantity."""
    
    assert (abs(Quantity(-1, Unit('m'))) ==
            abs(Quantity(1, Unit('m'))) ==
               Quantity(1, Unit('m')))
               
def test_bool():
    """Quantities are true if they are non-zero."""
    assert Quantity(1, Unit('m'))
    assert not Quantity(0, Unit('m'))
    
def test_complex():
    """Casting to complex drops the unit."""
    assert complex(Quantity(1, Unit('m'))) == complex(1)
    
def test_float():
    """Casting to float drops the unit."""
    assert float(Quantity(1, Unit('m'))) == float(1)
    
def test_hex():
    """Casting to hex string drops the unit."""
    assert hex(Quantity(1, Unit('m'))) == hex(1)
    
def test_int():
    """Casting to int drops the unit."""
    assert int(Quantity(1, Unit('m'))) == int(1)
    
def test_oct():
    """Casting to octal string drops the unit."""
    assert oct(Quantity(1, Unit('m'))) == oct(1)
    
def test_pow():
    """Exponentiation of quantities."""
    REGISTRY.clear()
    define_units()
    
    m_unit = Unit('m')
    m_quant = Quantity(2, m_unit)
    assert (m_quant ** 2 ==
            m_quant * m_quant ==
            pow(m_quant, 2))

    cm_unit = Unit('cm')
    cm_quant = Quantity(2, cm_unit)
    assert (cm_quant ** 2 ==
            cm_quant * cm_quant ==
            pow(cm_quant, 2))

REGISTRY.clear()

