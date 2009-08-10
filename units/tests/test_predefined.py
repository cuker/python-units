import units.predefined
from units import unit
import units

class TestPredefined(object):
    def setup_method(self, method):
        units.predefined.define_units()
        
    def test_predefined_simple_si(self):
        assert unit('m').si

    def test_predefined_complex_si(self):
        assert unit('Hz').si