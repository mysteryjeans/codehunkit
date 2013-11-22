"""
Codehunkit core models
@author: faraz@fanaticlab.com
"""

import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from codehunkit.db import models as db_models


class Language(models.Model):
    """
    Programming language
    """    
    name = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)    
    
    def __unicode__(self):
        return self.name


class LanguageGraph(models.Model):
    """
    Language graph of activites. Separate graph allows faster loading while updates runs on this table
    """
    language = models.OneToOneField(Language, primary_key=True, related_name='graph')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    subscriptions_count = models.IntegerField(default=0)
    coders_count = models.IntegerField(default=0)
    snippnets_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'app_language_graph'


class Location(models.Model):
    """
    Location
    """
    name = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=50, blank=True, null=True)    
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    def __unicode__(self):
        return self.name


class School(models.Model):
    """
    School of users
    """
    name = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    def __unicode__(self):
        return self.name


class SchoolGraph(models.Model):
    """
    School graph of user activaties, Separate graph allows faster loading while updates runs on this table
    """
    school = models.OneToOneField(School, primary_key=True, related_name='graph')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    coders_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'app_school_graph'
    

class User(AbstractUser):
    """
    Extended user more basic information
    """
    GENDERS = (('M', 'Male'),
               ('F', 'Female'))
        
    gender = models.CharField(max_length=1, choices=GENDERS)
    hometown = models.ForeignKey(Location, null=True, related_name='hometown_users')
    location = models.ForeignKey(Location, null=True)
    locale = models.CharField(max_length=10, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)


class UserGraph(models.Model):
    """
    User graph of his activities
    """
    user = models.OneToOneField(User, primary_key=True, related_name='graph')    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0) # Up votes received on user's snippets
    down_votes = models.IntegerField(default=0) # Down votes received on user's snippets
    snippets_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_user_graph'
    
    def __unicode__(self):
        return unicode(self.user)


class Education(models.Model):
    """
    User education
    """
    user = models.OneToOneField(User, primary_key=True)
    school = models.ForeignKey(School)
    degree = models.CharField(max_length=250, null=True)
    year = models.IntegerField(null=True)
    type = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)


class Snippet(models.Model):
    """
    Code snippet
    """
    id = db_models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User)
    gist = models.TextField(db_index=True)
    code = models.TextField(db_index=True)
    group = models.ForeignKey('self', null=True) # Allows to group together codes in different languages
    language = models.ForeignKey(Language)
    tags = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    rank = models.FloatField(default=0, db_index=True)
    comments_count = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    def __unicode__(self):
        return self.excerpt
    

class Comment(models.Model):
    """
    User's comment on snippent or reply on comment
    """
    id = db_models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User)
    snippet = models.ForeignKey(Snippet)
    reply_to = models.ForeignKey('self', null=True, blank=True)        
    comment_text = models.TextField()
    votes = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    rank = models.FloatField(default=0, db_index=True)
    replies_count = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    def __unicode__(self):
        return self.comment_text[:50] if self.comment_text else ''


class SnippetVote(models.Model):
    """
    User and snippet vote
    """
    user = models.ForeignKey(User)
    snippet = models.ForeignKey(Snippet)
    index = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_snippet_vote'
        unique_together = ('user', 'snippet')


class CommentVote(models.Model):
    """
    User and snippet vote
    """
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    index = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_comment_vote'
        unique_together = ('user', 'comment')


class Badge(models.Model):
    """
    User's badges based on expertness
    """    
    name = models.CharField(max_length=20)
    group_name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    badge_url = models.URLField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    def __unicode__(self):
        return self.name


class LanguageBadgeSummary(models.Model):
    """
    Summary of badges earn by language
    """
    language = models.ForeignKey(Language)
    badge = models.ForeignKey(Badge)
    badges_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_language_badge_summary'


class UserBadge(models.Model):
    """
    Badge earn by user
    """
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_user_badge'
        unique_together = ('user', 'badge',)


class SchoolBadgeSummary(models.Model):
    """
    Summary for badge earn by school students
    """
    school = models.ForeignKey(School)
    badge = models.ForeignKey(Badge)
    badges_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)
    
    class Meta:
        db_table = 'app_school_badge_summary'
        unique_together = ('school', 'badge',) 


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

        
class FacebookUser(models.Model):
    """
    Facebook user information
    """
    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    access_token = models.CharField(max_length=2048,blank=True,null=True) # Sizes can grow and shrink therefore 2K should be enough
    access_expiry = models.DateTimeField(blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=75)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.username
   

