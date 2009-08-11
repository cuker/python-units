"""Tests for addition and subtraction of Quantities"""


import py.test
from units import unit
import units.composed_unit
import units.named_composed_unit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

def test_good_simple_add():
    """Two quantities with the same unit should add together."""
    
    r = {}
    
    assert (Quantity(2, unit('m', registry=r)) + 
            Quantity(2, unit('m', registry=r)) == 
            Quantity(4, unit('m', registry=r)))
    
def add_bad():
    """Incompatible leaf units should not add together."""
    r = {}
    metres = Quantity(2, unit('m', registry=r))
    seconds = Quantity(2, unit('s', registry=r))
    return metres + seconds
    
def test_bad_simple_add():
    """Two quantities with different units should not add together."""
    py.test.raises(IncompatibleUnitsException, add_bad)

def test_good_simple_sub():
    """Should be able to subtract compatible Quantities."""
    r = {}
    assert (Quantity(4, unit('m', registry=r)) - 
            Quantity(2, unit('m', registry=r)) == 
            Quantity(2, unit('m', registry=r)))
    
def subtract_bad():
    """Incompatible leaf units should not subtract from one another."""
    r = {}
    metres = Quantity(2, unit('m', registry=r))
    seconds = Quantity(2, unit('s', registry=r))
    return metres - seconds
    
def test_bad_simple_sub():
    """Two quantities with different units should not allow subtraction."""
    py.test.raises(IncompatibleUnitsException, subtract_bad)

def test_good_composed_add():
    """Two quantities with the same complex units should add together"""
    r = {}
    assert (Quantity(2, unit('m', registry=r) / unit('s', registry=r)) +
            Quantity(3, unit('m', registry=r) / unit('s', registry=r)) ==
            Quantity(5, unit('m', registry=r) / unit('s', registry=r)))
    
def test_good_named_add():
    """Two quantities with the same named complex units should add together"""
    r = {}
    furlong = units.named_composed_unit.make(
                'furlong', 
                units.composed_unit.make([unit('m', registry=r)], 
                                         [], 
                                         multiplier=201.168,
                                         registry=r),
                is_si=False, registry=r) 
                
    assert (Quantity(2, furlong) +
            Quantity(2, furlong) ==
            Quantity(4, furlong))
                                       

def test_good_mixed_add():
    """Two quantities with the same units should add together 
    even if one is named"""
    r = {}
    gray = units.named_composed_unit.make(
            'gray',
            units.composed_unit.make([unit('J', registry=r), unit('kg', registry=r)],
                                     [], 
                                     registry=r),
            is_si=True, registry=r)
            
    sievert = units.composed_unit.make([unit('J', registry=r), unit('kg', registry=r)], [], registry=r)
    
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
    r = {}

    moon = units.composed_unit.make([unit('day', registry=r)], [], multiplier=28, registry=r)
    lunar_cycle = units.composed_unit.make([unit('day', registry=r)], [], multiplier=28, registry=r)
    
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
    
    r = {}
    mile = units.composed_unit.make([unit('m', registry=r)], [], multiplier=1609.344, registry=r)
    kilometre = units.composed_unit.make([unit('m', registry=r)], [], multiplier=1000, registry=r)   
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m', registry=r)))
    
def test_good_named_add_w_mults():
    """Two quantities with compatible but differently-named and 
    differently-multiplied units should add together."""
    r = {}
    mile = units.named_composed_unit.make(
            'mile', 
            units.composed_unit.make([unit('m', registry=r)], 
                                     [], 
                                     multiplier=1609.344, 
                                     registry=r), 
            registry=r)
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m', registry=r)], 
                                             [], 
                                             multiplier=1000, 
                                             registry=r), 
                    registry=r)
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m', registry=r)))    
    
def test_good_named_add_w_mult():
    """A quantity with a named composed unit that carries a multiplier 
    should add to a composed unit that has a multiplier"""
    r = {}
    mile = units.composed_unit.make([unit('m', registry=r)], [], multiplier=1609.344)
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m', registry=r)], 
                                             [], 
                                             multiplier=1000, 
                                             registry=r), 
                    registry=r)
                                               
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m', registry=r)))