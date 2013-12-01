"""
Context processors for codehunkit.com
"""

import datetime

from codehunkit.app.models import Language

def bootstrip(request):
    """
    Setting basic context variables
    """
    
    default_langs = Language.get_defaults()    
        
    return {
            'app_user': request.user,
            'hunkies': request.user.get_followings() if request.user.is_authenticated() else None,            
            'now': datetime.datetime.now(),
            'default_langs': default_langs,
    }
