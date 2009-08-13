"""Predefined units."""
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units import Unit
import units


def define_units():
    """Define built-in units.

    >>> define_units()
    >>> Unit('Hz').si
    True
    >>> Unit('m').si
    True
    >>> Unit('h').si
    False
    """
    define_base_si_units()
    define_complex_si_units()
    define_time_units()
    
    name("L", ['cm'] * 3, [], 1000)

def define_base_si_units():
    """Define the basic SI units.
    
    >>> define_base_si_units()
    >>> Unit('m').si
    True
    """
    # meter, gram, second, ampere, kelvin, mole, candela
    for sym in ["m", "g", "s", "A", "K", "mol", "cd"]:
        LeafUnit(sym, is_si=True)

def define_complex_si_units():
    """Define SI units that are built on other SI units.
    
    >>> define_complex_si_units()
    >>> Unit('Hz').si
    True
    """
    for sym in ["rad", "sr"]:  
        LeafUnit(sym, is_si=True)

    name("Hz", [], ["s"]) #hertz
    name("N", ["m", "kg"], ["s", "s"]) #Newton
    name("Pa", ["N"], ["m", "m"]) #pascal
    name("J", ["N", "m"], []) #Joule
    name("W", ["J"], ["s"]) # Watt
    name("C", ["s", "A"], []) # Coulomb
    name("V", ["W"], ["A"]) # Volt
    name("F", ["C"], ["V"]) # Farad
    name("Ohm", ["V"], ["A"]) 
    name("S", ["A"], ["V"])   #Siemens
    name("Wb", ["V", "s"], []) # Weber
    name("T", ["Wb"], ["m", "m"]) # Tesla
    name("H", ["Wb"], ["A"]) # Henry
    name("lm", ["cd", "sr"], []) # lumen 
    name("lx", ["lm"], ["m", "m"]) #lux
    name("Bq", [], ["s"]) # Becquerel
    name("Gy", ["J"], ["kg"]) # Gray
    name("Sv", ["J"], ["kg"]) # Sievert
    name("kat", ["mol"], ["s"]) # Katal
    
def define_time_units():
    """Define some common time units.
    
    >>> define_time_units()
    >>> hour = Unit('h')
    >>> hour.si
    False
    
    >>> from units.quantity import Quantity
    >>> half_hour = Quantity(0.5, hour)
    >>> few_secs = Quantity(60, Unit('s'))
    >>> sum = half_hour + few_secs
    
    >> mins = Unit('min')
    >> thirty_one = Quantity(31, mins)
    >> thirty_one == sum
    True
    """
    if not 's' in Unit.Registry:
        define_base_si_units()
    
    linear('min', 's', 60)
    linear('h', 'min', 60)
    linear('day', 'h', 24)
    
def name(symbol, 
         numer, 
         denom, 
         multiplier=1, 
         is_si=True):
    """Shortcut to create and return a new named unit."""
    return NamedComposedUnit(symbol,
            ComposedUnit([Unit(x) for x in numer], 
                         [Unit(x) for x in denom],
                         multiplier), 
            is_si)

def linear(new_symbol, base_symbol, multiplier):
    """Shortcut to create and return a new unit that is 
    a linear multiplication of another."""
    return NamedComposedUnit(new_symbol,
            ComposedUnit([Unit(base_symbol)],
                         [],
                         multiplier),
            is_si=False)
        