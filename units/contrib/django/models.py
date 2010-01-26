from django.db import models

from units import unit as Unit
from units.predefined import define_units
from units.quantity import Quantity
define_units()

__all__ = ('UnitField',)

class UnitProxy(Unit):
    def __init__(self, field, instance, quantity, unit):
        self.field = field
        self.instance = instance
        super(UnitProxy, self).__init__(quantity, unit)
    
    def _set_quantity(self, quantity):
        self._quantity = quantity
        setattr(self.instance, self.field.value_field, quantity)
        
    def _get_quantity(self):
        return self._quantity
    
    def _set_unit(self, unit):
        self._unit = unit
        setattr(self.instance, self.field.currency_field, strcurrency(unit))
        
    def _get_unit(self):
        return self._unit
        
    quantity = property(_get_quantity, _set_quantity)
    unit = property(_get_unit, _set_unit)

class UnitField(Field):
    
    description = "Django model field for a python unit object."
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, quantity, unit, *args, **kwargs):
        super(UnitField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if value in (None, ''):
            return None
        
        if isinstance(value, Quantity):
            return value
        
        qty, qty_unit = str(value).split()
        qty = float(qty)
        return unit(qty_unit)(qty)
    
    def get_internal_type(self):
        return 'CharField'