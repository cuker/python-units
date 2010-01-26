# -*- coding: utf-8 -*-
"""Predefined units."""
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units import unit, named_unit, scaled_unit

def define_units():
    """Define built-in units.
    
    >>> define_units()
    >>> unit('Hz').is_si()
    True
    >>> unit('m').is_si()
    True
    >>> unit('h').is_si()
    False
    """
    define_base_si_units()
    define_complex_si_units()
    define_time_units()
    define_volumes()
    define_imperial_units()
    define_astronomical_units()
    define_computer_units()
    define_ridiculous_units()

def define_base_si_units():
    """Define the basic SI units.
    
    >>> define_base_si_units()
    >>> unit('m').is_si()
    True
    """
    # Grabed from http://en.wikipedia.org/wiki/Conversion_of_units
    # TODO: Are these names differnet in another language?
    LeafUnit('m', name='metre', is_si=True) # Length, area, volume
    LeafUnit('g', name='gram', is_si=True) # Mass, Density
    LeafUnit('s', name='second', is_si=True) # Time
    LeafUnit('A', name='ampere', is_si=True) # Electric Current
    LeafUnit('K', name='kelvin', is_si=True) # Temperature
    LeafUnit('cd', name='candela', is_si=True) # Luminous intensity
    LeafUnit('mol', name='mole', is_si=True)
    
    scaled_unit('tonne', 'kg', 1000) # == 1Mg.

def define_complex_si_units():
    """Define SI units that are built on other SI units.
    
    >>> define_complex_si_units()
    >>> unit('Hz').is_si()
    True
    """
    LeafUnit('rad', name='radian', is_si=True) # Plane angle
    LeafUnit('sr', name='steradian', is_si=True)  #Solid angle
    
    named_unit('Hz', [], ['s'], name='hertz') # Frequency
    named_unit('N', ['m', 'kg'], ['s', 's'], name='newton') # Force
    named_unit('Pa', ['N'], ['m', 'm'], name='pascal') # Pressure or mechanical stress
    named_unit('J', ['N', 'm'], [], name='joule') # Energy, work, or amount of heat (Dangerous, 3J is a complex number)
    named_unit('W', ['J'], ['s'], name='watt') # Power or heat flow rate
    named_unit('C', ['s', 'A'], [], name='coulomb') # Electric charge
    named_unit('V', ['W'], ['A'], name='volt') # Electromotive force, electric potential difference
    named_unit('Ohm', ['V'], ['A'], symbal=u'Ω', name='ohm') # Electrical resistance
    named_unit('F', ['C'], ['V'], name='farad') # Capacitance
    named_unit('Wb', ['V', 's'], [], name='weber') # Magnetic flux
    named_unit('T', ['Wb'], ['m', 'm'], name='tesla') # Magnetic flux density
    named_unit('H', ['Wb'], ['A'], name='henry') # Inductance
    named_unit('lm', ['cd', 'sr'], [], name='lumen') # Luminous flux
    named_unit('lx', ['lm'], ['m', 'm'], name='lux') # Illuminance
    named_unit('Bq', [], ['s'], name='becquerel') # Radiation - source activity
    named_unit('Gy', ['J'], ['kg'], name='gray') # Radiation - absorbed dose
    named_unit('Sv', ['J'], ['kg'], name='sievert') # Radiation - equivalent dose
    named_unit('S', ['A'], ['V'], name='siemens') # Siemens
    named_unit('kat', ['mol'], ['s'], name='katal') # Katal
    

def define_time_units():
    """Define some common time units.
    
    >>> from units.compatibility import within_epsilon
    >>> define_base_si_units()
    >>> define_time_units()
    >>> hour = unit('h')
    >>> hour.is_si()
    False
    >>> from units.quantity import Quantity
    >>> half_hour = Quantity(0.5, hour)
    >>> few_secs = Quantity(60.0, unit('s'))
    >>> sum = half_hour + few_secs
    
    >>> mins = unit('min')
    >>> thirty_one = Quantity(31, mins)
    >>> within_epsilon(thirty_one, sum)
    True
    """
    assert unit('s').is_si() # Ensure SI units already defined.
    
    scaled_unit('min', 's', 60.0, name='minute')
    scaled_unit('h', 'min', 60.0, name='hour')
    scaled_unit('day', 'h', 24.0, symbal='d', name='day')
    scaled_unit('wk', 'day', 7.0, name='week')

def define_volumes():
    """Define some common kitchen volumes.
    
    
    >>> from units.quantity import Quantity
    >>> define_base_si_units()
    >>> define_volumes()
    >>> one_litre = Quantity(520, unit('mL')) + Quantity(2, unit('cups'))
    >>> one_litre == Quantity(1, unit('L'))
    True
    """
    # Dangerous unit, 3L gives a long int.
    assert unit('m').is_si()
    NamedComposedUnit('L', unit('dm') ** 3, is_si=True)
    
    scaled_unit('tsp', 'mL', 5.0)
    scaled_unit('tbsp', 'mL', 15.0)
    scaled_unit('cups', 'mL', 240.0)

def define_imperial_units():
    """Define some common imperial units."""
    
    assert unit('m').is_si() # Ensure SI units already defined
    
    # scaled_unit measures
    scaled_unit('inch', 'cm', 2.54, name='inch')
    scaled_unit('in', 'cm', 2.54, name='inch') # 'in' is a python keyword
    scaled_unit('ft', 'inch', 12.0, name='foot')
    scaled_unit('yd', 'ft', 3.0, name='yard')
    scaled_unit('fm', 'ft', 6.0, name='fathom')
    scaled_unit('rd', 'yd', 5.5, name='rod')
    scaled_unit('fur', 'rd', 40.0, name='furlong')
    scaled_unit('mi', 'fur', 8.0, name='mile')
    scaled_unit('lea', 'mi', 3.0, name='leage')
    
    # nautical scaled_unit measures
    scaled_unit('NM', 'm', 1852.0, name='nautical mile')
    scaled_unit('cable', 'NM', 0.1, name='cable length')
    
    # chain measure
    scaled_unit('li', 'inch', 7.92, name='link')
    scaled_unit('ch', 'li', 100.0, name='chain')
    
    # area measure
    NamedComposedUnit('acre', ComposedUnit([unit('rd')] * 2, [], 160.0), name='acre')
    
    # liquid measures
    NamedComposedUnit('pt', ComposedUnit([unit('inch')] * 3, [], 28.875), name='pint')
    
    scaled_unit('gi', 'pt', 0.25, name='gills')
    scaled_unit('qt', 'pt', 2.0, name='quarts')
    scaled_unit('gal', 'qt', 4.0, name='gallons')
    
    scaled_unit('fl oz', 'pt', 1.0 / 16.0, name='fluid ounce')
    scaled_unit('fl dr', 'fl oz', 1.0 / 8.0, name='fluid drachm')
    scaled_unit('minim', 'fl dr', 1.0 / 60.0, name='minim')
    
    # weight
    scaled_unit('oz', 'g', 28.375, name='ounce')
    scaled_unit('lb', 'oz', 16.0, name='pound')
    scaled_unit('ton', 'lb', 2000.0, name='ton')
    scaled_unit('grain', 'lb', 1.0 / 7000.0, name='grain')
    scaled_unit('dr', 'lb', 1.0 / 256.0, name='dram')
    scaled_unit('cwt', 'lb', 100.0, name='hundredweight')
    
    scaled_unit('dwt', 'grain', 24.0, name='pennyweight')
    scaled_unit('oz t', 'dwt', 20.0, name='ounce troy')
    scaled_unit('lb t', 'oz t', 12.0, name='pound troy')
    
    # power
    scaled_unit('hpl', 'W', 746.9999, name='mechanical')
    scaled_unit('hpm', 'W', 735.49875, name='metric horsepower')
    scaled_unit('hpe', 'W', 746.0, name='electric horsepower')
    
    # energy
    scaled_unit('BTU', 'J', 1055.056, name='ISO BTU', is_si=True)

def define_astronomical_units():
    """Define some astronomical units."""
    scaled_unit('ly', 'm', 9460730472580800, name='light-year')
    scaled_unit('AU', 'm', 149597870691, name='Astronomical unit')
    scaled_unit('pc', 'm', 3.08568025 * 10 ** 16, name='parsec', is_si=True)

def define_computer_units():
    """Define some units for technology.
    
    >>> define_units()
    >>> unit('GiB')(200) > unit('GB')(200) # bastard marketers
    True
    """
    
    NamedComposedUnit('flop', unit('operation') / unit('s'), name='flop', is_si=True)
    scaled_unit('B', 'bit', 8.0, name='byte', is_si=True)
    scaled_unit('KiB', 'B', 1024.0, name='kilobyte')
    scaled_unit('MiB', 'KiB', 1024.0, name='megabyte')
    scaled_unit('GiB', 'MiB', 1024.0, name='gigabyte')
    scaled_unit('TiB', 'GiB', 1024.0, name='terabyte')
    scaled_unit('PiB', 'TiB', 1024.0, name='petabyte')

def define_ridiculous_units():
    """Define some silly units.
    
    >>> define_units()
    >>> from units.quantity import Quantity
    >>> Quantity(1, unit('keg')) / Quantity(1, unit('bottle'))
    140.8450704225352
    """
    
    scaled_unit('firkin', 'lb', 90.0, name='firkin')
    scaled_unit('fortnight', 'day', 14.0, name='fortnight')
    
    scaled_unit('smoot', 'cm', 170.0, name='smoot')
    
    scaled_unit('hiroshima', 'J', 6.3 * 10.0 ** 13.0, name='hiroshima')
    
    scaled_unit('bottle', 'mL', 355.0, name='bottle')
    scaled_unit('keg', 'L', 50.0, name='keg')
        
        