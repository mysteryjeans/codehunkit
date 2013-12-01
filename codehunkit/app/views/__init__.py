from django.template import Context, RequestContext
from django.shortcuts import render_to_response

import urllib

from django.conf import settings
from django.core.urlresolvers import reverse


def render_response(request, *args, **kwargs):
    """
    Render template using RequestContext so that context processors should be available in template
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


def paginated_url(url_name, result_set, args, qs=None):
    """
    Returns previous and next page urls
    """
    prev_url = None
    next_url = None
    qs = '?' + urllib.urlencode(qs) if qs else ''
    page_index = int(args[-1])
    
    if page_index == 1:
        prev_url = reverse(url_name, args=args[:-1]) + qs
    elif page_index > 1 :
        args[-1] = page_index - 1
        prev_url = reverse(url_name, args=args) + qs
    
    if len(result_set) == settings.PAGE_SIZE:
        args[-1] = page_index + 1
        next_url = reverse(url_name, args=args) + qs
        
    return prev_url, next_url
    
