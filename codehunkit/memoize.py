"""
Decorators for caching func result
"""

from functools import wraps


def method(func):
    """
    Decorator for caching parameterless bound method
    """
    key = '_memoize_%s' % func.__name__
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, key):
            setattr(self, key, func(self))
        return getattr(self, key)
    
    return wrapper

