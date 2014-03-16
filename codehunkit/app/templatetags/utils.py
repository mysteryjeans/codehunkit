"""
Utility template tags
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
from django.template import Library


register = Library()

def jsonify(value):
    if isinstance(value, QuerySet):
        return mark_safe(serialize('json', value))
    return mark_safe(json.dumps(value))

register.filter('jsonify', jsonify)
jsonify.is_safe = True


@register.filter
def when(d, now=None):
    """
    Returns user friendly date difference with help of django timesince filter 
    """
    return timesince(d, now).split(',')[0]


@register.filter
def lines(value):
    return value.split('\n')