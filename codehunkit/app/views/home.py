"""
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import urllib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from codehunkit.app.views import render_response, paginated_url
from codehunkit.app.models import Snippet, User, Language



def index(request, page_index=0, sort_by_new=False):
    """
    Display all snippets
    """
    page_index = int(page_index)
    active = 'new' if sort_by_new else 'top'
    snippets = Snippet.get_snippets(request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    prev_url, next_url = paginated_url(request.resolver_match.url_name, snippets, [page_index])
    recent_sign_ups = User.get_recent_users()
    
    return render_response(request, 'app/home_snippets.html', locals())


def tag_snippets(request, tag_name, page_index=0, sort_by_new=False):
    """
    Display list of snippets by tag
    """
    page_index = int(page_index)
    active = 'new' if sort_by_new else 'top'
    snippets = Snippet.tag_snippets(tag_name, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    prev_url, next_url = paginated_url(request.resolver_match.url_name, snippets, [tag_name, page_index])
    
    return render_response(request, 'app/tag_snippets.html', locals())    
    
        
def search(request, page_index=0, sort_by_new=False):
    """
    Display snippets by user, language or search term
    """
    q = request.REQUEST.get('q', '').strip()
    if q:
        users_q = User.objects.filter(username__iexact=q)[:1]
        if users_q:            
            return HttpResponseRedirect(reverse('app_user', args=[users_q[0].username]))
        
        lang_q = Language.objects.filter(name__iexact=q)[:1]
        print lang_q
        if lang_q:
            print lang_q
            return HttpResponseRedirect(reverse('app_lang', args=[lang_q[0].slug]))
        
        page_index = int(page_index)
        params = { 'q': q.encode('utf-8')}
        query = '?' + urllib.urlencode(params)
        active = 'new' if sort_by_new else 'top'
        snippets = Snippet.search_snippets(q, request.user, page_index, settings.PAGE_SIZE, sort_by_new)                
        prev_url, next_url = paginated_url(request.resolver_match.url_name, snippets, [page_index], params)
        no_snippets = 'There are no snippets found for this search query'
                
        return render_response(request, 'app/search_snippets.html', locals())
    
    return HttpResponseRedirect(reverse('app_home'))

def sitemap_xml(request):
    """
    Display list of new snippets upto 1000
    """
    snippets = Snippet.get_snippets(request.user, 0, 1000, True)
    for snippet in snippets:
        snippet.priority = round(snippet.rating(), 1)
    return render_to_response('app/sitemap.xml', locals(), mimetype='application/xml')
