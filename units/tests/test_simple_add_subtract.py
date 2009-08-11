"""Tests for addition and subtraction of Quantities"""


import py.test
from units import unit
import units.composed_unit
import units.named_composed_unit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

def test_good_simple_add():
    """Two quantities with the same unit should add together."""
    
    registry = {}
    
    assert (Quantity(2, unit('m', registry=registry)) + 
            Quantity(2, unit('m', registry=registry)) == 
            Quantity(4, unit('m', registry=registry)))
    
def add_bad():
    """Incompatible leaf units should not add together."""
    registry = {}
    metres = Quantity(2, unit('m', registry=registry))
    seconds = Quantity(2, unit('s', registry=registry))
    return metres + seconds
    
def test_bad_simple_add():
    """Two quantities with different units should not add together."""
    py.test.raises(IncompatibleUnitsException, add_bad)

def test_good_simple_sub():
    """Should be able to subtract compatible Quantities."""
    registry = {}
    assert (Quantity(4, unit('m', registry=registry)) - 
            Quantity(2, unit('m', registry=registry)) == 
            Quantity(2, unit('m', registry=registry)))
    
def subtract_bad():
    """Incompatible leaf units should not subtract from one another."""
    registry = {}
    metres = Quantity(2, unit('m', registry=registry))
    seconds = Quantity(2, unit('s', registry=registry))
    return metres - seconds
    
def test_bad_simple_sub():
    """Two quantities with different units should not allow subtraction."""
    py.test.raises(IncompatibleUnitsException, subtract_bad)

def test_good_composed_add():
    """Two quantities with the same complex units should add together"""
    registry = {}
    assert (Quantity(2, unit('m', registry=registry) / 
                        unit('s', registry=registry)) +
            Quantity(3, unit('m', registry=registry) / 
                        unit('s', registry=registry)) ==
            Quantity(5, unit('m', registry=registry) / 
                        unit('s', registry=registry)))
    
def test_good_named_add():
    """Two quantities with the same named complex units should add together"""
    registry = {}
    furlong = units.named_composed_unit.make(
                'furlong', 
                units.composed_unit.make([unit('m', registry=registry)], 
                                         [], 
                                         multiplier=201.168,
                                         registry=registry),
                is_si=False, registry=registry) 
                
    assert (Quantity(2, furlong) +
            Quantity(2, furlong) ==
            Quantity(4, furlong))
                                       

def test_good_mixed_add():
    """Two quantities with the same units should add together 
    even if one is named"""
    registry = {}
    gray = units.named_composed_unit.make(
            'gray',
            units.composed_unit.make([unit('J', registry=registry), 
                                        unit('kg', registry=registry)],
                                     [], 
                                     registry=registry),
            is_si=True, registry=registry)
            
    sievert = units.composed_unit.make([unit('J', registry=registry), 
                                            unit('kg', registry=registry)], 
                                       [], 
                                       registry=registry)
    
    assert(Quantity(2, gray) + 
           Quantity(2, sievert) ==
           Quantity(4, gray))
           
    assert(Quantity(2, sievert) +
           Quantity(2, gray) ==
           Quantity(4, sievert))
            
    assert(Quantity(2, sievert) == Quantity(2, gray))

def test_good_add_w_mult():
    """Two quantities with same units should add together when
    they have the same multiplier"""
    registry = {}

    moon = units.composed_unit.make([unit('day', registry=registry)], 
                                    [], 
                                    multiplier=28, 
                                    registry=registry)
    lunar_cycle = units.composed_unit.make([unit('day', registry=registry)], 
                                           [], 
                                           multiplier=28, 
                                           registry=registry)
    
    assert(Quantity(1, moon) +
           Quantity(1, lunar_cycle) ==
           Quantity(2, moon))

    assert(Quantity(1, lunar_cycle) +
           Quantity(1, moon) ==
           Quantity(2, lunar_cycle))
           
    assert(Quantity(1, moon) == Quantity(1, lunar_cycle))
    
def test_good_add_w_mults():
    """Two quantities with compatible units should add together 
    even when they have different multipliers"""
    
    registry = {}
    mile = units.composed_unit.make([unit('m', registry=registry)], 
                                    [], 
                                    multiplier=1609.344, 
                                    registry=registry)
    kilometre = units.composed_unit.make([unit('m', registry=registry)], 
                                         [], 
                                         multiplier=1000, 
                                         registry=registry)   
    
    m_on_left = Quantity(1, mile) + Quantity(1, kilometre)
    km_on_left = Quantity(1, kilometre) + Quantity(1, mile)
    manual_sum = Quantity(2609.344, unit('m', registry=registry))
            
    assert m_on_left == km_on_left
    assert km_on_left == m_on_left
    assert manual_sum == m_on_left
    assert manual_sum == km_on_left
    assert m_on_left == manual_sum
    assert km_on_left == manual_sum
    
def test_good_named_add_w_mults():
    """Two quantities with compatible but differently-named and 
    differently-multiplied units should add together."""
    registry = {}
    mile = units.named_composed_unit.make(
            'mile', 
            units.composed_unit.make([unit('m', registry=registry)], 
                                     [], 
                                     multiplier=1609.344, 
                                     registry=registry), 
            registry=registry)
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m', registry=registry)], 
                                             [], 
                                             multiplier=1000, 
                                             registry=registry), 
                    registry=registry)
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m', registry=registry)))    
    
def test_good_named_add_w_mult():
    """A quantity with a named composed unit that carries a multiplier 
    should add to a composed unit that has a multiplier"""
    registry = {}
    mile = units.composed_unit.make([unit('m', registry=registry)], 
                                    [], 
                                    multiplier=1609.344)
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m', registry=registry)], 
                                             [], 
                                             multiplier=1000, 
                                             registry=registry), 
                    registry=registry)
                                               
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m', registry=registry)))