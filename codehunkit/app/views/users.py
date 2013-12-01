from django.db import transaction
from django.conf import settings
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from codehunkit.app.views import render_response
from codehunkit.app.models import User, Follow, Snippet


def user_snippets(request, username, page_index=0, sort_by_new=False):
    """
    Display snippets of particular user
    """       
    user = get_object_or_404(User, username=username)
    is_follower = Follow.is_follower(user, request.user)
    snippets = Snippet.user_snippets(user, request.user, page_index, settings.PAGE_SIZE, sort_by_new)
    return render_response(request, 'app/user_snippets.html', locals())


@login_required
@transaction.commit_on_success
def user_follow(request, username):
    """
    Follow the user
    """
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        Follow.follow(user, request.user)                
        return HttpResponseRedirect(user.get_absolute_url())
    
    raise Http404()


@login_required
@transaction.commit_on_success
def user_unfollow(request, username):
    """
    Unfollow the user
    """
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        Follow.unfollow(user, request.user)        
        return HttpResponseRedirect(user.get_absolute_url())

    raise Http404()
