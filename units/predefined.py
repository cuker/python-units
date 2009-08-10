"""Predefined units."""
import units.composed_unit
import units.leaf_unit
import units.named_composed_unit
from units import unit


def define_units():
    """Define built-in units."""
    define_base_si_units()
    define_complex_si_units()
    
    # TODO Areas

    name("L", ['cm'] * 3, [], 1000)

    # TODO imperial

    # TODO http://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement

    

def define_base_si_units():
    """Define the basic SI units."""
    # meter, gram, second, ampere, kelvin, mole, candela
    for sym in ["m", "g", "s", "A", "K", "mol", "cd"]:
        units.leaf_unit.make(sym, is_si=True)

def name(symbol, numer, denom, multiplier=1, is_si=True):
    """Shortcut to create and return a new named unit."""
    return units.named_composed_unit.make(symbol,
            units.composed_unit.make([unit(x) for x in numer], 
                                     [unit(x) for x in denom], 
                                     multiplier), 
            is_si)
    

def define_complex_si_units():
    """Define SI units that are built on other SI units."""
    # TODO Radians and steradians are weird units that equal 1.
    for sym in ["rad", "sr"]:  
        units.leaf_unit.make(sym, is_si=True)

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