"""Predefined units."""
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units import Unit, name, linear

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
    define_volumes()
    define_imperial_units()
    define_ridiculous_units()

def define_base_si_units():
    """Define the basic SI units.
    
    >>> define_base_si_units()
    >>> Unit('m').si
    True
    """
    # meter, gram, second, ampere, kelvin, mole, candela
    for sym in ["m", "g", "s", "A", "K", "mol", "cd"]:
        LeafUnit(sym, is_si=True)
    
    linear('tonne', 'kg', 1000) # == 1Mg. 

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
    name("J", ["N", "m"], []) #Joule # Dangerous unit, 3J gives a complex number
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
    
    >>> from units.compatibility import within_epsilon
    >>> define_base_si_units()
    >>> define_time_units()
    >>> hour = Unit('h')
    >>> hour.si
    False
    >>> from units.quantity import Quantity
    >>> half_hour = Quantity(0.5, hour)
    >>> few_secs = Quantity(60.0, Unit('s'))
    >>> sum = half_hour + few_secs
    
    >>> mins = Unit('min')
    >>> thirty_one = Quantity(31, mins)
    >>> within_epsilon(thirty_one, sum)
    True
    """
    assert Unit('s').si # Ensure SI units already defined.
    
    linear('min', 's', 60.)
    linear('h', 'min', 60.)
    linear('day', 'h', 24.)
    linear('wk', 'day', 7.)
    
def define_volumes():
    """Define some common kitchen volumes.
    
    
    >>> from units.quantity import Quantity
    >>> define_base_si_units()
    >>> define_volumes()
    >>> one_litre = Quantity(520, Unit('mL')) + Quantity(2, Unit('cups'))
    >>> one_litre == Quantity(1, Unit('L'))
    True
    """
    # Dangerous unit, 3L gives a long int.
    assert Unit('m').si
    NamedComposedUnit("L", Unit("cm") ** 3, is_si=True)     
    
    linear('tsp', 'mL', 5)
    linear('tbsp', 'mL', 15)
    linear('cups', 'mL', 240)
    
def define_imperial_units():
    """Define some common imperial units."""
    
    assert Unit('m').si # Ensure SI units already defined
    
    # linear measures
    linear('inch', 'cm', 2.54) # 'in' is a python keyword
    linear('ft', 'inch', 12) # foot
    linear('yd', 'ft', 3) # yard
    linear('fathom', 'ft', 6) 
    linear('rd', 'yd', 5.5) # rod
    linear('fur', 'rd', 40) # furlong
    linear('mi', 'fur', 8) # mile
    linear('league', 'mi', 3)

    # nautical linear measures
    linear('NM', 'm', 1852) # Nautical mile
    linear('cable', 'NM', 0.1)
    
    # chain measure
    linear('li', 'inch', 7.92) # link
    linear('ch', 'li', 100) # chain
    
    # area measure
    NamedComposedUnit('acre',
                      ComposedUnit([Unit('rd'), Unit('rd')],
                                   [],
                                   160))
                                   
    # liquid measures
    NamedComposedUnit('pt', 
                      ComposedUnit([Unit('inch')] * 3,
                                   [],
                                   28.875)) # pint
    
    linear('gi', 'pt', 0.25) # gills
    linear('qt', 'pt', 2) # quarts
    linear('gal', 'qt', 4) # gallons

    linear('fl oz', 'pt', 1.0 / 16)
    linear('fl dr', 'fl oz', 1.0 / 8)
    linear('minim', 'fl dr', 1.0 / 60)
    
    # weight
    
    linear('oz', 'g', 28.375)
    linear('lb', 'oz', 16)
    linear('ton', 'lb', 2000)
    linear('grain', 'lb', 1.0 / 7000)
    linear('dr', 'lb', 1.0 / 256) # dram
    linear('cwt', 'lb', 100) # hundredweight
    
    linear('dwt', 'grain', 24) # pennyweight
    linear('oz t', 'dwt', 20) # ounce troy
    linear('lb t', 'oz t', 12) # pound troy
    
    # power
    linear('hpl', 'W', 746.9999) # mechanical
    linear('hpm', 'W', 735.49875) # metric horsepower
    linear('hpe', 'W', 746) # electric horsepower.
    
    # energy
    linear('BTU', 'J', 1055.056, is_si=True) # ISO BTU


def define_ridiculous_units():
    """Define some silly units.
    
    
    >>> define_units()
    >>> from units.quantity import Quantity
    >>> Quantity(1, Unit('keg')) / Quantity(1, Unit('bottle'))
    140.8450704225352
    """
    
    linear('firkin', 'lb', 90)
    linear('fortnight', 'day', 14)
    
    linear('ly', 'm', 9460730472580800) # light-year
    linear('AU', 'm', 149597870691) # Astronomical unit
    linear('pc', 'm', 3.08568025 * 10 ** 16, is_si=True) # parsec

    linear('smoot', 'cm', 170)
    
    linear('hiroshima', 'J', 6.3 * 10 ** 13)
    
    NamedComposedUnit('flop', Unit('operation') / Unit('s'), is_si=True)
    linear('B', 'bit', 8, is_si=True)  # byte
    
    linear('bottle', 'mL', 355)
    linear('keg', 'L', 50)    

        