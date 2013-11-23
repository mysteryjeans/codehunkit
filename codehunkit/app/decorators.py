"""
Decorators for codehunkit app
"""

from django.conf import settings
from django.http import HttpResponseRedirect

def anonymous_required(view_function, redirect_to=None):
    return AnonymousRequired(view_function, redirect_to)

class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to) 
        return self.view_function(request, *args, **kwargs)
