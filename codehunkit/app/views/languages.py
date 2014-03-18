from django.db import transaction
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from codehunkit.app.views import render_response, paginated_url
from codehunkit.app.models import Language, Subscription, Snippet


def lang_snippets(request, slug, page_index=0, sort_by_new=False):
    """
    Displays list of snippets of the particular language
    """
    page_index = int(page_index)
    active = 'new' if sort_by_new else 'top'
    lang = get_object_or_404(Language, slug=slug)
    is_subscribed = request.user.is_authenticated() and Subscription.is_subscribed(lang, request.user)
    snippets = Snippet.lang_snippets(lang, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    prev_url, next_url = paginated_url(request.resolver_match.url_name, snippets, [slug, page_index])
    
    return render_response(request, 'app/lang_snippets.html', locals())


@login_required
@transaction.commit_on_success
def lang_subscribe(request, slug):
    """
    Subscribe user to language
    """
    lang = get_object_or_404(Language, slug=slug)
    if request.method == 'POST':  
        Subscription.subscribe(lang, request.user)
            
    return HttpResponseRedirect(lang.get_absolute_url())


@login_required
@transaction.commit_on_success
def lang_unsubscribe(request, slug):
    """
    Unsubscribe user to language
    """
    lang = get_object_or_404(Language, slug=slug)
    if request.method == 'POST':
        Subscription.unsubscribe(lang, request.user)
    
    return HttpResponseRedirect(lang.get_absolute_url())