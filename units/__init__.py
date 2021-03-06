"""Provides support for quantities and units, which strictly disallow
invalid operations between incompatible quantities. For example, we cannot add
2 metres to 5 seconds, because this doesn't make sense.

Why?

From Wikipedia:

The Mars Climate Orbiter was intended to enter orbit at an altitude of
140-150 km (460,000-500,000 ft.) above Mars. However, a navigation error
caused the spacecraft to reach as low as 57 km (190,000 ft.). The spacecraft
was destroyed by atmospheric stresses and friction at this low altitude. The
navigation error arose because a NASA subcontractor (Lockheed Martin) used
Imperial units (pound-seconds) instead of the metric system.

Installation
============

This module is distributed via PyPI. So, you can do::
 
 pip install units

or::
 
 easy_install units

or, you can download a bundle yourself at http://pypi.python.org/pypi/units/

If you want the latest::
 
 pip install -e hg+http://www.arandonohue.com/hg/units#egg=units
 

How to Use
==========

Make Quantities
---------------

Units are objects that you use to make quantities::
  
  >>> from units import unit
  >>> metre = unit('m')
  >>> print(metre(7) + metre(11))
  18 m

You can mix and match these quantities in some ways::
  
  >>> from units import unit
  >>> metre = unit('m')
  >>> second = unit('s')
  >>> print(metre(10) / second(2))
  5 m / s
  >>> print(metre(10) ** 3)
  1000 m * m * m

But if you make a mistake, you get a safety net::
  
  >>> from units import unit
  >>> unit('m')(5) + unit('s')(5)
  Traceback (most recent call last):
  ...
  IncompatibleUnitsError

Make Your Own Units
-------------------
Before you start making your own units, you should check out the units that
you get for free::
  
  >>> import units.predefined
  >>> units.predefined.define_units()

It includes all the official SI units, some units for measuring time such as
days and weeks, units for volumes like cups, gallons and litres, imperial
units and more.

You've already seen how to make your own simple units. You call
the unit function and give it a string::
  
  >>> from units import unit
  >>> blog = unit('blog')
  >>> print(blog(3))
  3 blog

These units are automatically incompatible with other units.

You can combine units with multiplication and division to make new units::
  
  >>> from units import unit
  >>> blogs_per_network = unit('blog') / unit('network')
  >>> print(blogs_per_network(2.34))
  2.34 blog / network

There's a built-in shortcut for making new units that are scalar multiples
of other units::
  
  >>> from units import unit, scaled_unit
  >>> sickle = scaled_unit('sickle', 'knut', 29)
  >>> galleon = scaled_unit('galleon', 'sickle', 17)
  >>> knut = unit('knut')
  >>> galleon(3.0) + sickle(1.0) - knut(25.0) == knut(1483)
  True

There's also a shortcut for giving names to slightly more complicated units::
  
  >>> from units import unit, named_unit
  >>> from units.predefined import define_units
  >>> define_units()
  >>> twp = named_unit('tweetpack', ['tweet', 'meme'], ['day'], 5)
  >>> # A tweetpack is 5 tweetmemes per day
  >>> print(twp(2))
  2 tweetpack
  >>> tweet, meme, day = [unit(x) for x in ['tweet', 'meme', 'day']]
  >>> print(twp(5) - (tweet(5) * meme(4) / day(2)))
  3.0 tweetpack

If two units are compatible, you can convert between them easily::
  
  >>> from units import unit
  >>> from units.predefined import define_units
  >>> define_units()
  >>> furlongs_per_fortnight = unit('fur') / unit('fortnight')
  >>> kph = unit('km') / unit('h')
  >>> print(furlongs_per_fortnight(kph(100)))
  167024.576473 fur / fortnight

You can also use lower-level constructors to make your own units and
quantities. The ways shown above are easier, though.

Warnings
--------

This module doesn't solve problems with numerical accuracy or
floating point conversions::
  
  >>> from units import unit
  >>> unit('m')(5) / unit('m')(7)
  0

More dangerously, certain internal operations have implicit arithmetic
that can surprise you::
  
  >>> from units import unit, scaled_unit
  >>> sickle = scaled_unit('sickle', 'knut', 29)
  >>> galleon = scaled_unit('galleon', 'sickle', 17)
  >>> knut = unit('knut')
  >>> galleon(3) + sickle(1) - knut(25) == galleon(3)
  True


Using Modified Python
---------------------

In units-enhanced Python, you can do::
  
  print(2cm / 0.5 s)
  -> 4.0 cm / s

Units-enhanced Python is a version of PyPy with built-in support
for units. You can find it in the unitPython directory. Essentially,
apply the supplied patches to r66797 of PyPy. If you're on a suitable
UNIX, the included unitPython/unitPython.sh does this for you.

@requires: U{Python<http://python.org/>} >= 2.5
@since: 2009-Aug-10
@status: under development
"""

__author__    = 'Aran Donohue'
__version__   = '0.03'
__copyright__ = '2009'
__license__   = 'Python Software Foundation License'
__contact__   = 'aran@arandonohue.com'

import units.si
from units.composed_unit import ComposedUnit
from units.leaf_unit import LeafUnit
from units.named_composed_unit import NamedComposedUnit
from units.registry import REGISTRY

def unit(specifier, symbal=u'', name=u'', is_si=False):
    """Main factory for units.
    
    >>> unit('m') == unit('m')
    True
    >>> unit('m') != unit('s')
    True
    """
    if specifier in REGISTRY:
        return REGISTRY[specifier]
    elif units.si.can_make(specifier):
        return units.si.prefixed_unit(specifier)
    else:
        return LeafUnit(specifier, symbal, name, is_si)

def named_unit(specifier, numer, denom, multiplier=1, symbal=u'', name=u'', is_si=True):
    """Shortcut to create and return a new named unit."""
    
    numer_units = [unit(x) for x in numer]
    denom_units = [unit(x) for x in denom]
    
    return NamedComposedUnit(specifier, ComposedUnit(numer_units, denom_units, multiplier), symbal, name, is_si)

def scaled_unit(specifier, base_specifier, multiplier, symbal=u'', name=u'', is_si=False):
    """Shortcut to create and return a new unit that is
    a scaled_unit multiplication of another."""
    return NamedComposedUnit(specifier, ComposedUnit([unit(base_specifier)], [], multiplier), symbal, name, is_si)