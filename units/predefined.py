"""Predefined units."""
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units import Unit
import units


def define_units(registry=units.Unit.Registry):
    """Define built-in units.

    >>> registry = {}
    >>> define_units(registry)
    >>> Unit('Hz', registry).si
    True
    >>> Unit('m', registry).si
    True
    """
    define_base_si_units(registry)
    define_complex_si_units(registry)
    
    name("L", ['cm'] * 3, [], 1000, registry=registry)

def define_base_si_units(registry):
    """Define the basic SI units.
    
    >>> registry = {}
    >>> define_base_si_units(registry=registry)
    >>> Unit('m', registry).si
    True
    """
    # meter, gram, second, ampere, kelvin, mole, candela
    for sym in ["m", "g", "s", "A", "K", "mol", "cd"]:
        LeafUnit(sym, is_si=True, registry=registry)

def name(symbol, 
         numer, 
         denom, 
         multiplier=1, 
         is_si=True, 
         registry=units.Unit.Registry):
    """Shortcut to create and return a new named unit."""
    return NamedComposedUnit(symbol,
            ComposedUnit([Unit(x) for x in numer], 
                                     [Unit(x) for x in denom], 
                                     multiplier,
                                     registry), 
            is_si,
            registry)
    

def define_complex_si_units(registry):
    """Define SI units that are built on other SI units.
    
    >>> registry = {}
    >>> define_complex_si_units(registry)
    >>> Unit('Hz', registry).si
    True
    """
    for sym in ["rad", "sr"]:  
        LeafUnit(sym, is_si=True, registry=registry)

    name("Hz", [], ["s"], registry=registry) #hertz
    name("N", ["m", "kg"], ["s", "s"], registry=registry) #Newton
    name("Pa", ["N"], ["m", "m"], registry=registry) #pascal
    name("J", ["N", "m"], [], registry=registry) #Joule
    name("W", ["J"], ["s"], registry=registry) # Watt
    name("C", ["s", "A"], [], registry=registry) # Coulomb
    name("V", ["W"], ["A"], registry=registry) # Volt
    name("F", ["C"], ["V"], registry=registry) # Farad
    name("Ohm", ["V"], ["A"], registry=registry) 
    name("S", ["A"], ["V"], registry=registry)   #Siemens
    name("Wb", ["V", "s"], [], registry=registry) # Weber
    name("T", ["Wb"], ["m", "m"], registry=registry) # Tesla
    name("H", ["Wb"], ["A"], registry=registry) # Henry
    name("lm", ["cd", "sr"], [], registry=registry) # lumen 
    name("lx", ["lm"], ["m", "m"], registry=registry) #lux
    name("Bq", [], ["s"], registry=registry) # Becquerel
    name("Gy", ["J"], ["kg"], registry=registry) # Gray
    name("Sv", ["J"], ["kg"], registry=registry) # Sievert
    name("kat", ["mol"], ["s"], registry=registry) # Katal