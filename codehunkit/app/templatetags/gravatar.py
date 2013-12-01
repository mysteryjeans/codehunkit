"""
User's picture to social profile links tags
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab 
"""

from django import template
import urllib, hashlib
 
register = template.Library()
 
class GravatarUrlNode(template.Node):
    def __init__(self, user, size=None):
        self.user = template.Variable(user)
        self.size = template.Variable(size) if size else None
 
    def render(self, context):
        try:
            user = self.user.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        
        if not self.size:
            self.size = 40
        
        if hasattr(user, 'fb_id') and user.fb_id:
            return u'http://graph.facebook.com/%s/picture?width=%s&height=%s' % (user.fb_id, self.size, self.size)
        
        default = "identicon"        
        size = self.size.resolve(context) if self.size else 40
 
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size), 'r':'g'})
 
        return gravatar_url


class GravatarProfileUrlNode(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)
 
    def render(self, context):
        try:
            user = self.user.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        
        if hasattr(user, 'fb_id'):
            return u'http://www.facebook.com/%s' % user.fb_id
  
        gravatar_url = "http://www.gravatar.com/" + hashlib.md5(user.email.lower()).hexdigest()
                 
        return gravatar_url

 
@register.tag
def gravatar_url(parser, token):
    
    tokens = token.split_contents()
    
    if len(tokens) == 2:
        tag_name, user = tokens
        return GravatarUrlNode(user)
    else:
        tag_name, user, size = tokens
        return GravatarUrlNode(user, size)            
    
    raise template.TemplateSyntaxError, "%r tag requires a user and optional size arguments" % token.contents.split()[0]


@register.tag
def gravatar_profile_url(parser, token):
    try:
        tag_name, user = token.split_contents()
 
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
 
    return GravatarProfileUrlNode(user)