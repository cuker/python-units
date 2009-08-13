"""Test inequality comparisons between QUANTITIES, such as
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
try:
    import py.test
except ImportError:
    pass
    
from units import Unit
from units.composed_unit import ComposedUnit
from units.named_composed_unit import NamedComposedUnit
from units.quantity import Quantity
from units.exception import IncompatibleUnitsException

CVEL = Unit('m') / Unit('s')

VEL = NamedComposedUnit("VEL", CVEL)

COMPATIBLE_QUANTITIES = [[Quantity(0, VEL), Quantity(1, VEL)],
                         [Quantity(0, CVEL), Quantity(1, CVEL)]]

ALL_UNITS = [Unit('m') / Unit('s'), 
             Unit('m') * Unit('s'), 
             Unit('m'), Unit('s'),
             NamedComposedUnit("Hz", ComposedUnit([], [Unit('s')])),
             NamedComposedUnit("L", 
                               ComposedUnit([Unit('m')] * 3, 
                                            [], 
                                            multiplier=0.001))]

QUANTITIES = [[Quantity(n, u) for n in [0, 1]] for u in ALL_UNITS]
FLAT_QUANTITIES = sum(QUANTITIES, [])

def less_than(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 < quant2

def less_than_or_eq(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 <= quant2

def greater_than_or_eq(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 >= quant2

def greater_than(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 > quant2

def equal(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 == quant2

def not_equal(quant1, quant2):
    """Binary function to call the operator"""
    return quant1 != quant2 and quant2 != quant1

def test_lt(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert less_than(quant1, quant2)

def test_lte(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert less_than_or_eq(quant1, quant2)

def test_gte(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert greater_than_or_eq(quant1, quant2)

def test_gt(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert greater_than(quant1, quant2)

def test_eq(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert equal(quant1, quant2)

def test_ne(quant1, quant2):
    """Binary function to assert the operator's result"""
    assert not_equal(quant1, quant2)

def test_invalid_lt(quant1, quant2):
    """Binary function to assert the operator's exception"""
    py.test.raises(IncompatibleUnitsException, less_than, quant1, quant2)

def test_invalid_lte(quant1, quant2):
    """Binary function to assert the operator's exception"""
    py.test.raises(IncompatibleUnitsException, less_than_or_eq, quant1, quant2)

def test_invalid_gte(quant1, quant2):
    """Binary function to assert the operator's exception"""
    py.test.raises(IncompatibleUnitsException, 
                   greater_than_or_eq, 
                   quant1, 
                   quant2)

def test_invalid_gt(quant1, quant2):
    """Binary function to assert the operator's exception"""
    py.test.raises(IncompatibleUnitsException, greater_than, quant1, quant2)

def test_invalid_eq(quant1, quant2):
    """Binary function to assert the operator's exception"""
    equal(quant1, quant2)


def pytest_generate_tests(metafunc):
    """Py.test test case generation."""
    # Valid comparisons
    if metafunc.function == test_eq:
        for quant in FLAT_QUANTITIES:
            metafunc.addcall(funcargs=dict(quant1=quant, quant2=quant))
        
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[0][0], 
                                       quant2=COMPATIBLE_QUANTITIES[1][0]))
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[1][0], 
                                       quant2=COMPATIBLE_QUANTITIES[0][0]))
            
    
    if metafunc.function == test_ne:
        for i, elem1 in enumerate(FLAT_QUANTITIES):
            for j, elem2 in enumerate(FLAT_QUANTITIES):
                if j > i:
                    metafunc.addcall(funcargs=dict(quant1=elem1, quant2=elem2))
    
    if metafunc.function == test_gte:
        for quant in FLAT_QUANTITIES:
            metafunc.addcall(funcargs=dict(quant1=quant, quant2=quant))
        
        for q_group in QUANTITIES:
            lesser, greater = tuple(q_group)
            metafunc.addcall(funcargs=dict(quant1=greater, quant2=lesser))
        
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[0][1], 
                                       quant2=COMPATIBLE_QUANTITIES[1][0]))
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[1][1], 
                                       quant2=COMPATIBLE_QUANTITIES[0][0]))
    
    if metafunc.function == test_gt:
        for q_group in QUANTITIES:
            lesser, greater = tuple(q_group)
            metafunc.addcall(funcargs=dict(quant1=greater, quant2=lesser))
        
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[0][1], 
                                       quant2=COMPATIBLE_QUANTITIES[1][0]))
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[1][1], 
                                       quant2=COMPATIBLE_QUANTITIES[0][0]))
        
    
    if metafunc.function == test_lte:
        for quant in FLAT_QUANTITIES:
            metafunc.addcall(funcargs=dict(quant1=quant, quant2=quant))
        
        for q_group in QUANTITIES:
            lesser, greater = tuple(q_group)
            metafunc.addcall(funcargs=dict(quant1=lesser, quant2=greater))
        
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[1][0], 
                                       quant2=COMPATIBLE_QUANTITIES[0][1]))
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[0][0], 
                                       quant2=COMPATIBLE_QUANTITIES[1][1]))

    
    if metafunc.function == test_lt:
        for q_group in QUANTITIES:
            lesser, greater = tuple(q_group)
            metafunc.addcall(funcargs=dict(quant1=lesser, quant2=greater))
        
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[1][0],
                                       quant2=COMPATIBLE_QUANTITIES[0][1]))
        metafunc.addcall(funcargs=dict(quant1=COMPATIBLE_QUANTITIES[0][0],
                                       quant2=COMPATIBLE_QUANTITIES[1][1]))
            
    
    if metafunc.function == test_invalid_eq:
        for i, elem1 in enumerate(FLAT_QUANTITIES):
            for j, elem2 in enumerate(FLAT_QUANTITIES):
                if j > i:
                    metafunc.addcall(funcargs=dict(quant1=i, quant2=j))
    
    if metafunc.function in [test_invalid_gte,
                             test_invalid_gt,
                             test_invalid_lte,
                             test_invalid_lt]:
        for i, q_group1 in enumerate(QUANTITIES):
            for j, q_group2 in enumerate(QUANTITIES):
                if j > i:
                    metafunc.addcall(funcargs=dict(quant1=q_group1[0],
                                                   quant2=q_group2[0]))

Unit.Registry.clear()
assert len(Unit.Registry) == 0