"""
Snippet views
"""


import logging

from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from codehunkit.app import HunkitError
from codehunkit.app.views import render_response
from codehunkit.app.models import Snippet, Tag
from codehunkit.app.forms import SnippetForm


logger = logging.getLogger('django.request')

    
@login_required
@transaction.commit_on_success
def create_snippet(request):
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

        
