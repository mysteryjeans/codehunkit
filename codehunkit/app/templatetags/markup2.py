"""
Text to Markup filters 
"""


import markdown2 as md2
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown2(value):
    return mark_safe(md2.markdown(force_unicode(value)))

#register.filter(md2_to_html, 'md2_to_html')