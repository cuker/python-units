"""Tests for addition and subtraction of Quantities"""


import py.test
from units import unit
import units.composed_unit
import units.named_composed_unit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

def test_good_simple_add():
    """Two quantities with the same unit should add together."""
    assert (Quantity(2, unit('m')) + 
            Quantity(2, unit('m')) == 
            Quantity(4, unit('m')))
    
def add_bad():
    """Incompatible leaf units should not add together."""
    metres = Quantity(2, unit('m'))
    seconds = Quantity(2, unit('s'))
    return metres + seconds
    
def test_bad_simple_add():
    """Two quantities with different units should not add together."""
    py.test.raises(IncompatibleUnitsException, add_bad)

def test_good_simple_sub():
    """Should be able to subtract compatible Quantities."""
    assert (Quantity(4, unit('m')) - 
            Quantity(2, unit('m')) == 
            Quantity(2, unit('m')))
    
def subtract_bad():
    """Incompatible leaf units should not subtract from one another."""
    metres = Quantity(2, unit('m'))
    seconds = Quantity(2, unit('s'))
    return metres - seconds
    
def test_bad_simple_sub():
    """Two quantities with different units should not allow subtraction."""
    py.test.raises(IncompatibleUnitsException, subtract_bad)

def test_good_composed_add():
    """Two quantities with the same complex units should add together"""
    assert (Quantity(2, unit('m') / unit('s')) +
            Quantity(3, unit('m') / unit('s')) ==
            Quantity(5, unit('m') / unit('s')))
    
def test_good_named_add():
    """Two quantities with the same named complex units should add together"""
    furlong = units.named_composed_unit.make(
                'furlong', 
                units.composed_unit.make([unit('m')], 
                                         [], 
                                         multiplier=201.168),
                is_si=False) 
                
    assert (Quantity(2, furlong) +
            Quantity(2, furlong) ==
            Quantity(4, furlong))
                                       

def test_good_mixed_add():
    """Two quantities with the same units should add together 
    even if one is named"""
    gray = units.named_composed_unit.make(
            'gray',
            units.composed_unit.make([unit('J'), unit('kg')],
                                     []),
            is_si=True)
            
    sievert = units.composed_unit.make([unit('J'), unit('kg')], [])
    
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

    moon = units.composed_unit.make([unit('day')], [], multiplier=28)
    lunar_cycle = units.composed_unit.make([unit('day')], [], multiplier=28)
    
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
    
    mile = units.composed_unit.make([unit('m')], [], multiplier=1609.344)
    kilometre = units.composed_unit.make([unit('m')], [], multiplier=1000)   
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m')))
    
def test_good_named_add_w_mults():
    """Two quantities with compatible but differently-named and 
    differently-multiplied units should add together."""
    
    mile = units.named_composed_unit.make(
            'mile', 
            units.composed_unit.make([unit('m')], 
                                     [], 
                                     multiplier=1609.344))
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m')], 
                                             [], 
                                             multiplier=1000))
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m')))    
    
def test_good_named_add_w_mult():
    """A quantity with a named composed unit that carries a multiplier 
    should add to a composed unit that has a multiplier"""
    
    mile = units.composed_unit.make([unit('m')], [], multiplier=1609.344)
    kilometre = units.named_composed_unit.make(
                    'km',
                    units.composed_unit.make([unit('m')], 
                                             [], 
                                             multiplier=1000))
                                               
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m')))        