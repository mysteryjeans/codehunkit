"""
Utility template tags
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""


from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
from django.template import Library


register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True


@register.filter
def when(d, now=None):
    """
    Returns user friendly date difference with help of django timesince filter 
    """
    return timesince(d, now).split(',')[0]