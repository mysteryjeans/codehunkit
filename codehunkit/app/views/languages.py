from django.db import transaction
from django.conf import settings
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from codehunkit.app.views import render_response
from codehunkit.app.models import Language, Subscription, Snippet


def lang_snippets(request, slug, page_index=0, sort_by_new=False):
    """
    Displays list of snippets of the particular language
    """
    lang = get_object_or_404(Language, slug=slug)
    is_subscribed = request.user.is_authenticated() and Subscription.is_subscribed(lang, request.user)
    snippets = Snippet.lang_snippets(lang, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/lang_snippets.html', locals())


@login_required
@transaction.commit_on_success
def lang_subscribe(request, slug):
    """
    Subscribe user to language
    """
    if request.method == 'POST':
        lang = get_object_or_404(Language, slug=slug)
        Subscription.subscribe(lang, request.user)
        return HttpResponseRedirect(lang.get_absolute_url())
            
    raise Http404()


@login_required
@transaction.commit_on_success
def lang_unsubscribe(request, slug):
    """
    Unsubscribe user to language
    """
    if request.method == 'POST':
        lang = get_object_or_404(Language, slug=slug)
        Subscription.unsubscribe(lang, request.user)
        return HttpResponseRedirect(lang.get_absolute_url())
            
    raise Http404()