"""Tests for addition and subtraction of Quantities"""


import py.test
from units import unit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

def test_valid_simple_addition():
    """Two quantities with the same unit should add together."""
    assert (Quantity(2, unit('m')) + 
            Quantity(2, unit('m')) == 
            Quantity(4, unit('m')))
    
def add_invalid():
    metres = Quantity(2, unit('m'))
    seconds = Quantity(2, unit('s'))
    return metres + seconds
    
def test_invalid_simple_addition():
    """Two quantities with different units should not add together."""
    py.test.raises(IncompatibleUnitsException, add_invalid)

def test_valid_simple_subtraction():
    """Should be able to subtract compatible Quantities."""
    assert (Quantity(4, unit('m')) - 
            Quantity(2, unit('m')) == 
            Quantity(2, unit('m')))
    
def subtract_invalid():
    metres = Quantity(2, unit('m'))
    seconds = Quantity(2, unit('s'))
    return metres - seconds
    
def test_invalid_simple_subtraction():
    """Two quantities with different units should not allow subtraction."""
    py.test.raises(IncompatibleUnitsException, subtract_invalid)

def test_valid_composed_addition():
    """Two quantities with the same complex units should add together"""
    assert (Quantity(2, unit('m') / unit('s')) +
            Quantity(3, unit('m') / unit('s')) ==
            Quantity(5, unit('m') / unit('s')))
    
def test_valid_named_composed_addition():
    """Two quantities with the same named complex units should add together"""
    furlong = named_composed_unit.make('furlong', 
                                       composed_unit.make(['m'], 
                                                          [], 
                                                          multiplier=201.168),
                                       si=False) 
    assert (Quantity(2, furlong) +
            Quantity(2, furlong) ==
            Quantity(4, furlong))
                                       

def test_valid_mixed_named_composed_addition():
    """Two quantities with the same units should add together 
    even if one is named"""
    gray = named_composed_unit.make('gray',
                                    composed_unit.make(['J', 'kg'],
                                                       []),
                                    si=True)
    sievert = composed_unit.make(['J', 'kg'], [])
    
    assert(Quantity(2, gray) + 
           Quantity(2, sievert) ==
           Quantity(4, gray))
           
    assert(Quantity(2, sievert) +
           Quantity(2, gray) ==
           Quantity(4, sievert))
            
    assert(Quantity(2, sievert) == Quantity(2, gray))

def test_valid_composed_addition_with_multiplier():
    """Two quantities with same units should add together when
    they have the same multiplier"""

    moon = composed_unit.make(['day'], [], multiplier=28)
    lunar_cycle = composed_unit.make(['day'], [], multiplier=28)
    
    assert(Quantity(1, moon) +
           Quantity(1, lunar_cycle) ==
           Quantity(2, moon))

    assert(Quantity(1, lunar_cycle) +
           Quantity(1, moon) ==
           Quantity(2, lunar_cycle))
           
    assert(Quantity(1, moon) == Quantity(1, lunar_cycle))
    
def test_valid_composed_addition_with_multipliers():
    """Two quantities with compatible units should add together 
    even when they have different multipliers"""
    
    mile = composed_unit.make(['m'], [], multiplier=1609.344)
    kilometre = composed_unit.make(['m'], [], multiplier=1000)   
    
    assert(Quantity(1, mile) + Quantity(1, kilometre) ==
           Quantity(1, kilometre) + Quantity(1, mile) ==
           Quantity(2609.344, unit('m')))
    
def test_valid_named_composed_addition_with_multipliers():
    """Two quantities with compatible but differently-named and 
    differently-multiplied units should add together."""
    pass
    
def test_valid_named_composed_addition_with_multiplier():
    """A quantity with a named composed unit that carries a multiplier 
    should add to a composed unit that has a multiplier"""
    pass
    #left 
    #right