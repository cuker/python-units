"""Tests for the predefined units"""

import units.predefined
from units import unit
import units

class TestPredefined(object):
    """Test class to allow py.test to use the setup_method."""
    def setup_method(self, method):
        """Called before individual tests"""
        self.registry = {}
        units.predefined.define_units(registry=self.registry)
        
    def test_predefined_simple_si(self):
        """Simple predefined units like metres should be marked as SI"""
        assert unit('m', registry=self.registry).si

    def test_predefined_complex_si(self):
        """Complex predefined units like Hz should be marked as SI"""
        assert unit('Hz', registry=self.registry).si