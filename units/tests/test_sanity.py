"""Simple fast sanity check to ensure that the basics are functional.
Canary for a completely-broken setup."""
#!/usr/bin/env python

from units import unit

def test_basic_creation():
    """The unit() method should construct equal unit objects 
    given equal strings."""
    
    r = {}
    assert unit('m', registry=r) == unit('m', registry=r)

def test_basic_difference():
    """The unit() method should construct different unit objects
    given different strings."""
    r = {}
    assert unit('m', registry=r) != unit('s', registry=r)