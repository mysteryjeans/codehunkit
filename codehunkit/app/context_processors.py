"""
Context processors for codehunkit.rootplugin.com
"""

import datetime

from codehunkit.app.models import Language, FlashMessage

def bootstrip(request):
    """
    Setting basic context variables
    """
    default_langs = Language.get_defaults()
    return {
            'app_user': request.user,
            'hunkies': request.user.get_followings() if request.user.is_authenticated() else None,            
            'now': datetime.datetime.now(),
            'langs': request.user.get_langs() if request.user.is_authenticated() else default_langs,
            'default_langs': default_langs,
            'flash_messages': FlashMessage.get_messages(request.user) if request.user.is_authenticated() else None
    }
