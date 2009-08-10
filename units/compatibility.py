"""Check the compatibility of units."""

def compatible(unit1, unit2):
    """True iff quantities in the given units can be interchanged 
    for some multiplier.
    """
    return unit1.canonical() == unit2.canonical()