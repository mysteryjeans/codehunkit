"""
Snippets listing views
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import urllib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse

from codehunkit.app.views import render_response


logger = logging.getLogger('django.request')


def home(request, by_new=False, page_index=0):
    return render_response(request, 'app/home.html')


def language(request, slug):
    """
    Displays list of snippets of the particular language
    """
    
        
def search(request):
    """
    Display snippets by user, language or search term
    """


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
    
