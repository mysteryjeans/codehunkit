from django.db import transaction
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from codehunkit.app.views import render_response, paginated_url
from codehunkit.app.models import User, Follow, Snippet


def user_snippets(request, username, page_index=0, sort_by_new=False):
    """
    Display snippets of particular user
    """
    page_index = int(page_index)
    active = 'new' if sort_by_new else 'top'
    user = get_object_or_404(User, username=username)
    is_follower = request.user.is_authenticated() and Follow.is_follower(user, request.user)
    snippets = Snippet.user_snippets(user, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    prev_url, next_url = paginated_url(request.resolver_match.url_name, snippets, [username, page_index])

    return render_response(request, 'app/user_snippets.html', locals())


@login_required
@transaction.commit_on_success
def user_follow(request, username):
    """
    Follow the user
    """
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        Follow.follow(user, request.user)                
    
    return HttpResponseRedirect(user.get_absolute_url())


@login_required
@transaction.commit_on_success
def user_unfollow(request, username):
    """
    Unfollow the user
    """
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        Follow.unfollow(user, request.user)        
    
    return HttpResponseRedirect(user.get_absolute_url())
