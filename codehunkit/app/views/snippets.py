import urllib

from django.db import transaction
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from codehunkit.app import HunkitError
from codehunkit.app.views import render_response
from codehunkit.app.models import Snippet, SnippetVote, Comment, CommentVote, Tag
from codehunkit.app.forms import SnippetForm


def snippet_read(request, snippet_id, slug=None):
    """
    Display Snippet
    """
    if slug is None:
        snippet = get_object_or_404(Snippet, id=snippet_id)
        return HttpResponsePermanentRedirect(snippet.get_absolute_url())
    
    snippet_id = int(snippet_id)
    snippet = Snippet.read(snippet_id, request.user)
    return render_response(request, 'app/snippet.html', locals())

    
@login_required
@transaction.commit_on_success
def snippet_create(request):
    """
    Creates a new code snippet
    """
    tags = [tag.name for tag in Tag.get_tags()]
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                snippet = Snippet.create(data['gist'], data['code'], data['language'], data['tags'], request.user)
                return HttpResponseRedirect('/')  #return HttpResponseRedirect(snippet.get_absolute_url())
            except HunkitError as e:
                error = e.message
    else:
        form = SnippetForm()
    
    return render_response(request, 'app/create_snippet.html', locals())


@transaction.commit_on_success
def snippet_vote(request, snippet_id, action):
    """
    Vote-UP/DOWN a snippet
    """
    if request.method == 'POST':        
        snippet_id = int(snippet_id)        
        if request.user.is_anonymous():
            return HttpResponseForbidden(reverse('app_login') + '?' + urllib.urlencode({'next': reverse('app_snippet_read', args=[snippet_id])}))
                
        if action == 'UP':
            vote_index, net_effect = SnippetVote.vote_up(request.user, snippet_id)
        elif action == 'DOWN':
            vote_index, net_effect = SnippetVote.vote_down(request.user, snippet_id)
        else:
            raise Http404()
        
        if request.is_ajax():
            response = {'snippet_id': snippet_id, 'vote_index': vote_index, 'net_effect':net_effect }
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
            
        return HttpResponseRedirect(reverse('app_snippet_read', args=[snippet_id]))
    
    raise Http404()

        
def comment_read(request, snippet_id, comment_id):
    """
    Display Snippet with particular comment thread
    """
    snippet_id = int(snippet_id)
    comment_id = int(comment_id)
    snippet = Snippet.read(snippet_id, request.user, comment_id)
    return render_response(request, 'app/snippet.html', locals())


@login_required
@transaction.commit_on_success
def comment_create(request, snippet_id):
    """
    Creates a new comment for snippet
    """
    if request.method == 'POST':
        snippet_id = int(snippet_id)
        comment_text = request.POST.get('comment_text', None)        
        if comment_text:            
            snippet = Snippet.objects.get(id=snippet_id)
            comment = Comment.save_comment(request.user, snippet_id, comment_text[:settings.MAX_COMMENT_LENGTH])        
            if request.is_ajax():
                return render_response(request, 'app/parts/comment.html', { 'snippet': snippet, 'comment': comment })        
            
            return HttpResponseRedirect(reverse('app_snippet_read', args=[snippet_id]) + '#comment-id-' + str(comment.id))    
    
    raise Http404()


@login_required
@transaction.commit_on_success
def reply_create(request, snippet_id, comment_id):
    """
    Saves a new reply for comment
    """
    if request.method == 'POST':
        snippet_id = int(snippet_id)
        comment_id = int(comment_id)
        comment_text = request.POST.get('comment_text', None)        
        if comment_text:            
            snippet = Snippet.objects.get(id=snippet_id)
            comment = Comment.save_reply(request.user, snippet_id, comment_id, comment_text[:settings.MAX_COMMENT_LENGTH])        
            if request.is_ajax():
                return render_response(request, 'app/parts/comment.html', { 'snippet': snippet, 'comment': comment })        
            
            return HttpResponseRedirect(reverse('app_snippet_read', args=[snippet_id]) + '#comment-id-' + str(comment.id))    
    
    raise Http404()


@transaction.commit_on_success
def comment_vote(request, snippet_id, comment_id, action):
    """
    Vote-UP/DOWN a comment
    """
    if request.method == 'POST':        
        snippet_id = int(snippet_id)
        comment_id = int(comment_id)        
        if request.user.is_anonymous():
            return HttpResponseForbidden(reverse('app_login') + '?' + urllib.urlencode({'next': reverse('app_snippet_read', args=[snippet_id])}))
                
        if action == 'UP':
            vote_index, net_effect = CommentVote.vote_up(request.user, comment_id)
        elif action == 'DOWN':
            vote_index, net_effect = CommentVote.vote_down(request.user, comment_id)
        else:
            raise Http404()
        
        if request.is_ajax():
            response = {'comment_id': comment_id, 'vote_index': vote_index, 'net_effect':net_effect }
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
            
        return HttpResponseRedirect(reverse('app_snippet_read', args=[snippet_id]))
    
    raise Http404()
