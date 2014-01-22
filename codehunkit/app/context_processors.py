"""
Context processors for codehunkit.com
"""

import datetime

from codehunkit.app.models import Language

def bootstrip(request):
    """
    Setting basic context variables
    """
    
    return {
            'app_user': request.user,
            'hunkies': request.user.get_followings() if request.user.is_authenticated() else None,            
            'now': datetime.datetime.now(),
            'langs': request.user.get_langs() if request.user.is_authenticated() else Language.get_defaults(),
    }
