"""
Database fields for PostgreSQL
@author: faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext as _

__version__ = "1.0"
__author__ = "faraz@fanaticlab.com"


class BigAutoField(models.AutoField):
    """
    8 bytes auto increment data type field
    """    
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return "bigint AUTO_INCREMENT"
        elif 'oracle' in connection.__class__.__module__:
            return "NUMBER(19)"
        elif 'postgresql' in connection.__class__.__module__:
            return "bigserial"
        
        raise NotImplementedError('BigAutoField doesn''t support database %s' % connection.__class__.__module__)
    
    def get_internal_type(self):
        return "BigAutoField"
    
    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(_("This value must be a long integer."))
    
    def get_prep_value(self, value):
        if value is None:
            return None
        return long(value)

# References for BigAutoField were resolved to data type of integer, which wasn't appropiate 
class _ForeignKey(models.ForeignKey):
    """
    Fix 8 bytes auto increment data type reference column in tables
    """    
    def db_type(self, connection):
        rel_field = self.rel.get_related_field()
        if isinstance(rel_field, BigAutoField):
            return models.BigIntegerField().db_type(connection=connection)
        
        return super(_ForeignKey, self).db_type(connection=connection)
models.ForeignKey = _ForeignKey
    
    
# citext extension must be install to support this field in PostgreSQL
class CITextField(models.TextField):
    """
    citext data type for case insensitive comparison in PostgreSQL  
    """
    def db_type(self, connection):        
        if 'postgresql' in connection.__class__.__module__:
            return 'citext'
            
        raise NotImplementedError('CITextField (citext db type) is only supported for PostgreSQL')


# citext extension must be install to support this field in PostgreSQL
class CIEmailField(models.EmailField):
    """
    citext data type for case insensitive email comparison in PostgreSQL  
    """
    def db_type(self, connection):        
        if 'postgresql' in connection.__class__.__module__:
            return 'citext'
            
        raise NotImplementedError('CITextField (citext db type) is only supported for PostgreSQL')