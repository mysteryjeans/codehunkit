"""
User messages
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

from django.db import models

from codehunkit.db import models as db_models
from codehunkit.app.models.core import User
from codehunkit.app.models.snippets import Snippet, Comment

class Notification(models.Model):
    """
    User persistent messages
    """
    MESSAGE_TYPES = (('CO', 'Comment'),
                     ('RE', 'Reply'),
                     ('TE', 'Text'),)
    
    id = db_models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sent_message')
    snippet = models.ForeignKey(Snippet, null=True)
    comment = models.ForeignKey(Comment, null=True)
    comment_msg = models.ForeignKey(Comment, null=True, related_name='comment_msg')
    message_type = models.CharField(max_length=2, choices=MESSAGE_TYPES)
    message_text = models.CharField(max_length=1024, null=True, blank=True)
    read_on = models.DateTimeField(null=True, blank=True)
    viewed_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=75)
    
    class Meta:
        index_together = [['id', 'user', 'read_on', 'viewed_on']]
    
    def __unicode__(self):
        return '[user_id: %s, type: %s]' % (self.user_id, self.message_type)
            

class FlashMessage(models.Model):
    """
    Store flash messages for user
    """
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'
    SUCCESS = 'success'
    FLASH_TYPES = ((INFO, 'Information'),
                   (ERROR, 'Error'),
                   (WARNING, 'Warning'),
                   (SUCCESS, 'Success'),)
    
    id = db_models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User)
    flash_text = models.TextField()
    flash_type = models.CharField(max_length=10,choices=FLASH_TYPES)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=75)
    
    class Meta:
        db_table = 'app_flash_message'
    
    def __unicode__(self):
        return self.flash_text
    
    @classmethod
    def add_message(cls, flash_type, flash_text, user):
        """
        Adds a new message for user in database
        """
        return cls.objects.create(flash_type=flash_type, flash_text=flash_text, user=user, created_by=str(user))
    
    @classmethod
    def add_info(cls, flash_text, user):
        """
        Adds a new info message for user in database
        """
        return cls.add_message(cls.INFO, flash_text, user)
    
    @classmethod
    def add_error(cls, flash_text, user):
        """
        Adds a new error message for user in database
        """
        return cls.add_message(cls.ERROR, flash_text, user)
    
    @classmethod
    def add_warning(cls, flash_text, user):
        """
        Adds a new warning message for user in database
        """
        return cls.add_message(cls.WARNING, flash_text, user)
    
    @classmethod
    def add_success(cls, flash_text, user):
        """
        Adds a new success message for user in database
        """
        return cls.add_message(cls.SUCCESS, flash_text, user)
    
    @classmethod
    def peek_messages(cls, user):
        """
        Returns all flash messages for user but don't delete them in database
        """        
        return [flash for flash in cls.objects.filter(user=user).order_by('flash_id')]

    @classmethod
    def get_messages(cls, user):
        """
        Returns all flash messages for user and delete them database
        """
        messages = cls.peek_messages(user)        
        cls.objects.filter(user=user).delete()
        return messages