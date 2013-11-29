"""
Snippets listing views
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import urllib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from codehunkit.app.views import render_response
from codehunkit.app.models import User, Language, Snippet

logger = logging.getLogger('django.request')


def home(request, page_index=0, sort_by_new=False):
    """
    Display all snippets
    """
    snippets = Snippet.get_snippets(request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/home_snippets.html', {'snippets': snippets})


def lang_snippets(request, slug, page_index=0, sort_by_new=False):
    """
    Displays list of snippets of the particular language
    """
    lang = get_object_or_404(Language, slug=slug)
    snippets = Snippet.lang_snippets(lang, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/lang_snippets.html', locals())
    

def tag_snippets(request, tag_name, page_index=0, sort_by_new=False):
    """
    Display list of snippets by tag
    """
    snippets = Snippet.tag_snippets(tag_name, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/tag_snippets.html', locals())    
    

def user_snippets(request, username, page_index=0, sort_by_new=False):
    """
    Display snippets of particular user
    """       
    user = User.objects.get(username=username)
    snippets = Snippet.user_snippets(user, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/user_snippets.html', locals())
        
def search(request, page_index=0, sort_by_new=False):
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
    
