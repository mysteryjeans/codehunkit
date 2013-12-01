"""
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

from django.conf import settings
from codehunkit.app.views import render_response
from codehunkit.app.models import Snippet


def index(request, page_index=0, sort_by_new=False):
    """
    Display all snippets
    """
    snippets = Snippet.get_snippets(request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/home_snippets.html', {'snippets': snippets})


def tag_snippets(request, tag_name, page_index=0, sort_by_new=False):
    """
    Display list of snippets by tag
    """
    snippets = Snippet.tag_snippets(tag_name, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/tag_snippets.html', locals())    
    
        
def search(request, page_index=0, sort_by_new=False):
    """
    Display snippets by user, language or search term
    """