"""Tests for the Python built-in functions when applied
to Quantities.
"""

from units.predefined import define_units
from units.quantity import Quantity
from units import Unit

def test_abs():
    assert (abs(Quantity(-1, Unit('m'))) ==
            abs(Quantity(1, Unit('m'))) ==
               Quantity(1, Unit('m')))
               
def test_bool():
    assert Quantity(1, Unit('m'))
    assert not Quantity(0, Unit('m'))
    
def test_complex():
    assert complex(Quantity(1, Unit('m'))) == complex(1)
    
def test_float():
    assert float(Quantity(1, Unit('m'))) == float(1)
    
def test_hex():
    assert hex(Quantity(1, Unit('m'))) == hex(1)
    
def test_int():
    assert int(Quantity(1, Unit('m'))) == int(1)
    
def test_oct():
    assert oct(Quantity(1, Unit('m'))) == oct(1)
    
def test_pow():
    Unit.Registry.clear()
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

Unit.Registry.clear()
assert len(Unit.Registry) == 0

