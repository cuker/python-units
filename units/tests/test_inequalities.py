"""Test inequality comparisons between quantities, such as
quantity < quantity
quantity <= quantity
quantity > quantity
quantity >= quantity

...
each of these * {leaf units, the various composed units, named units}, 
and each combination therein
...

each of these * valid and invalid comparisons

...
"""

import py.test

from units import Unit
from units.composed_unit import ComposedUnit
from units.named_composed_unit import NamedComposedUnit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

cvel = Unit('m') / Unit('s')

vel = NamedComposedUnit("vel", cvel)

compatible_quantities = [[Quantity(0, vel), Quantity(1, vel)],
                         [Quantity(0, cvel), Quantity(1, cvel)]]

all_units = [Unit('m') / Unit('s'), Unit('m') * Unit('s'), Unit('m'), Unit('s'),
             NamedComposedUnit("Hz", ComposedUnit([], [Unit('s')])),
             NamedComposedUnit("L", ComposedUnit([Unit('m')] * 3, [], multiplier=0.001))]

quantities = [[Quantity(n, u) for n in [0,1]] for u in all_units]
flat_quantities = sum(quantities, [])

def lt(x,y):
    return x < y

def lte(x, y):
    return x <= y
    
def gte(x, y):
    return x >= y
    
def gt(x, y):
    return x > y

def eq(x, y):
    return x == x
    
def ne(x, y):
    return x != y and y != x

def test_lt(x, y):
    assert lt(x, y)
    
def test_lte(x, y):
    assert lte(x, y)
    
def test_gte(x, y):
    assert gte(x, y)
    
def test_gt(x, y):
    assert gt(x, y)

def test_eq(x, y):
    assert eq(x, y)
    
def test_ne(x, y):
    assert ne(x, y)

def test_invalid_lt(x, y):
    py.test.raises(IncompatibleUnitsException, lt, x, y)
    
def test_invalid_lte(x, y):
    py.test.raises(IncompatibleUnitsException, lte, x, y)
    
def test_invalid_gte(x, y):
    py.test.raises(IncompatibleUnitsException, gte, x, y)
    
def test_invalid_gt(x, y):
    py.test.raises(IncompatibleUnitsException, gt, x, y)

def test_invalid_eq(x, y):
    eq(x, y)


def pytest_generate_tests(metafunc):
    # Valid comparisons
    if metafunc.function == test_eq:
        for q in flat_quantities:
            metafunc.addcall(funcargs=dict(x=q, y=q))
            
        metafunc.addcall(funcargs=dict(x=compatible_quantities[0][0], y=compatible_quantities[1][0]))
        metafunc.addcall(funcargs=dict(x=compatible_quantities[1][0], y=compatible_quantities[0][0]))
        
            
    if metafunc.function == test_ne:
        for i, elem1 in enumerate(flat_quantities):
            for j, elem2 in enumerate(flat_quantities):
                if j > i:
                    metafunc.addcall(funcargs=dict(x=i, y=j))
            
    if metafunc.function == test_gte:
        for q in flat_quantities:
            metafunc.addcall(funcargs=dict(x=q, y=q))
            
        for q_group in quantities:
            a,b = tuple(q_group)
            metafunc.addcall(funcargs=dict(x=b, y=a))
            
        metafunc.addcall(funcargs=dict(x=compatible_quantities[0][1], y=compatible_quantities[1][0]))
        metafunc.addcall(funcargs=dict(x=compatible_quantities[1][1], y=compatible_quantities[0][0]))

    if metafunc.function == test_gt:
        for q_group in quantities:
            a,b = tuple(q_group)
            metafunc.addcall(funcargs=dict(x=b, y=a))
            
        metafunc.addcall(funcargs=dict(x=compatible_quantities[0][1], y=compatible_quantities[1][0]))
        metafunc.addcall(funcargs=dict(x=compatible_quantities[1][1], y=compatible_quantities[0][0]))
        
        
    if metafunc.function == test_lte:
        for q in flat_quantities:
            metafunc.addcall(funcargs=dict(x=q, y=q))

        for q_group in quantities:
            a,b = tuple(q_group)
            metafunc.addcall(funcargs=dict(x=a, y=b))

        metafunc.addcall(funcargs=dict(x=compatible_quantities[1][0], y=compatible_quantities[0][1]))
        metafunc.addcall(funcargs=dict(x=compatible_quantities[0][0], y=compatible_quantities[1][1]))


    if metafunc.function == test_lt:
        for q_group in quantities:
            a,b = tuple(q_group)
            metafunc.addcall(funcargs=dict(x=a, y=b))
            
        metafunc.addcall(funcargs=dict(x=compatible_quantities[1][0], y=compatible_quantities[0][1]))
        metafunc.addcall(funcargs=dict(x=compatible_quantities[0][0], y=compatible_quantities[1][1]))
        
            
    if metafunc.function == test_invalid_eq:
        for i, elem1 in enumerate(flat_quantities):
            for j, elem2 in enumerate(flat_quantities):
                if j > i:
                    metafunc.addcall(funcargs=dict(x=i, y=j))
                                
    if metafunc.function in [test_invalid_gte,
                             test_invalid_gt,
                             test_invalid_lte,
                             test_invalid_lt]:            
        for i, q_group1 in enumerate(quantities):
            for j, q_group2 in enumerate(quantities):
                if j > i:
                    metafunc.addcall(funcargs=dict(x=q_group1[0], y=q_group2[0]))
            
