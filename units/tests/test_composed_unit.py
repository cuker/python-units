"""Tests specific to composed units and their complexities."""

from units import Unit
from units.composed_unit import ComposedUnit
from units.registry import REGISTRY

def test_unbox_to_num():
    """Test that composed units collapse properly to numbers."""
    assert ComposedUnit([Unit('m')], [Unit('m')], 8) == 8
    
def test_unbox_to_leaf():
    """Test that composed units collaple properly to leaf units."""
    assert ComposedUnit([Unit('m')], []) == Unit('m')
    
REGISTRY.clear()