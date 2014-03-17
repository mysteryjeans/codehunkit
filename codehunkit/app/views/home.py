"""
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import urllib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from codehunkit.app.views import render_response
from codehunkit.app.models import Snippet, User, Language



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
    q = request.REQUEST.get('q', None)
    if q:
        q = q.strip()
        
        users_q = User.objects.filter(username__iexact=q)[:1]
        if users_q:            
            return HttpResponseRedirect(reverse('app_user', args=[users_q[0].username]))
        
        lang_q = Language.objects.filter(name__iexact=q)[:1]
        if lang_q:            
            return HttpResponseRedirect(reverse('app_lang', args=[lang_q[0].name]))
        
        params = { 'q': q.encode('utf-8')}
        query = '?' + urllib.urlencode(params)
        source = {'title': q,
                  'absolute_url': reverse('app_search') + query,
                  'absolute_url_by_new': reverse('app_search_new') + query,
                  'active': 'new' if sort_by_new else 'top'}
        #posts = Post.tag_posts(q, int(page_index), settings.PAGE_SIZE, sort_by_new, request.app_user)
                
        #top_tags = Tag.top_tags()
        #top_channels = Channel.top_channels()                
        #prev_url, next_url = paginated_url(request.resolver_match.url_name, posts, [page_index], params)
                
        #return render_response(request, 'app/search.html', locals())
    
    return HttpResponseRedirect(reverse('app_home'))
