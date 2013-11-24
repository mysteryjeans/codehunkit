"""
Context processors for codehunkit.com
"""

from codehunkit.app.models import Language

def bootstrip(request):
    """
    Setting basic context variables
    """
    
    default_langs = Language.get_defaults()    
        
    return {
            'default_langs': default_langs,
    }
