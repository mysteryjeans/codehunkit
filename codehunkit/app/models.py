"""
Codehunkit core models
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import re
import random
import hashlib
import datetime

from django.db import models, connection
from django.db.models import F, Q 
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from codehunkit.app import CodeHunkitError
from codehunkit.db import models as db_models


class Language(models.Model):
    """
    Programming language
    """    
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(max_length=100)    
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        """
        Returns permanent link of lang
        """
        return ('app_lang', (self.slug,))
    
    @classmethod
    def get_all(cls):
        """
        Returns list of all languages
        """
        return list(cls.objects.order_by('name'))
    
    @classmethod
    def get_defaults(cls):
        """
        Returns list of default languages
        """
        return list(cls.objects.filter(is_default=True).order_by('name'))
    

class LanguageGraph(models.Model):
    """
    Language graph of activites. Separate graph allows faster loading while updates runs on this table
    """
    language = models.OneToOneField(Language, primary_key=True, related_name='graph')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    subscriptions_count = models.IntegerField(default=0)
    coders_count = models.IntegerField(default=0)
    snippets_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'app_language_graph'
    
    def __unicode__(self):
        return unicode(self.language)


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
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(unique=True)
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
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = ((MALE, 'Male'),
               (FEMALE, 'Female'))
        
    gender = models.CharField(max_length=1, choices=GENDERS)
    hometown = models.ForeignKey(Location, null=True, related_name='hometown_users', blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    locale = models.CharField(max_length=10, blank=True, null=True)
    has_activated = models.BooleanField(default=False)    
    activation_code = models.CharField(max_length=512, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = [ 'email', 'updated_by', 'created_by', 'has_activated']
    
    def activate(self):
        """
        Activate user account if not activated
        """
        User.objects.filter(id=self.id, has_activated=False).update(has_activated=True, updated_by=str(self))
                
    def change_password(self, password, new_password):        
        """
        Change user's password
        """
        if not self.check_password(password):            
            raise CodeHunkitError('Wrong password! please enter your current password again.')
        
        self.set_password(new_password)
    
        
    @classmethod 
    def sign_up(cls, username, email, password, gender, hometown=None, location=None, locale=None, is_verified=False):
        """
        Creates a new non-admin user in database 
        """            
        try:
            user = cls.objects.get(Q(username=username) | Q(email=email))
            if user.username == username:
                raise CodeHunkitError('Username "%s" already registered with us, if you forgotten your password? <a href="%s">Request new one</a> or choose a different username.' % (username, reverse('app_forgot_password')))
            
            raise CodeHunkitError('Its seems to be that you are already registered with this email address, if you forgotten your password? <a href="%s">Request new one.</a>' % reverse('app_forgot_password'))            
        except cls.DoesNotExist:
                        
            activation_code = None
            if not is_verified:            
                algo = hashlib.md5()
                algo.update(str(random.randrange(100, 10000000)))
                activation_code = algo.hexdigest()
            
            if hometown: 
                hometown = Location.objects.get_or_create(name=hometown)
            
            if location:
                location = Location.objects.get_or_create(name=location)
                
            user = cls.objects.create_user(username=username,
                                           email=email,
                                           password=password,
                                           gender= gender,
                                           hometown=hometown,
                                           location=location,
                                           locale=locale,
                                           has_activated=is_verified,
                                           activation_code=activation_code,
                                           updated_by=email,
                                           created_by=email)
            
            UserGraph.objects.create(user=user, created_by=email)
            
            # Create subscriptions to default languages
            langs = []
            for lang in Language.objects.filter(is_default=True):
                langs.append(lang.id)
                Subscription.objects.create(user=user,language=lang, created_by=email)
            
            if langs:
                LanguageGraph.objects.filter(language_id__in=langs).updated(subscriptions_count=F('subscriptions_count') + 1)
                
            return user
    

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
    created_by = models.CharField(max_length=100)
    
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


class Subscription(models.Model):
    """
    User subscription for languages
    """
    user = models.ForeignKey(User)
    language = models.ForeignKey(Language)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('user', 'language')
        

class Snippet(models.Model):
    """
    Code snippet
    """
    id = db_models.BigAutoField(primary_key=True)
    slug = models.SlugField()
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
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.gist
    
    @classmethod
    def get_snippets(cls, user, page_index, page_size, sort_by_new):
        """
        Returns all snippets
        """
        if sort_by_new:
            sql_query = '''
                        SELECT s.*, u.username, l.name, v.index as vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.sinppet_id AND v.user_id = %s
                        ORDER BY s.id DESC
                        LIMIT %s OFFSET %s
                        '''
        else:
            sql_query = '''
                        SELECT s.*, u.username, l.name, v.index as vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.sinppet_id AND v.user_id = %s
                        ORDER BY s.rank DESC, s.id DESC
                        LIMIT %s OFFSET %s
                        '''
            
        return [snippet for snippet in cls.objects.raw(sql_query, [user.user_id, page_size, page_index * page_size])]
    
    @classmethod
    def create(cls, gist, code, language_id, tags, user):
        """
        Creates a new code snippet in database
        """
        language = Language.objects.get(id=language_id)
        tags = tags.split(',')
        if language.name in tags: tags.remove(language.name)                
        tags = Tag.clean_tags(tags)
        
        snippet = cls.objects.create(gist=gist,
                                     slug=slugify(gist),
                                     user=user,
                                     code=code,
                                     language=language,
                                     tags=tags,
                                     updated_by=str(user),
                                     created_by=str(user))
        
        Tag.add_tags(tags, user)
        LanguageGraph.objects.filter(language_id=language.id).update(snippets_count=F('snippets_count') + 1)
        UserGraph.objects.filter(user_id=user.id).update(snippets_count=F('snippets_count') + 1)
        
        return snippet
        
    
    
    

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
    name = models.CharField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    description = models.TextField()
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


class Tag(models.Model):    
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    is_muted = models.BooleanField(default=False)    
    is_default = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=75)

    def __unicode__(self):
        return unicode(self.name)
        
    @models.permalink
    def get_absolute_url(self):
        """
        Returns absolute tag url
        """
        return ('app_tag', (self.name,))
    
    @classmethod
    def add_tags(cls, tags, user):
        """
        Create new tags in database if doesn't exists
        """        
        sql = '''INSERT INTO app_tag (name, is_muted, is_default, updated_by, updated_on) 
                 SELECT %s, false, false, %s, %s WHERE NOT EXISTS (SELECT 1 FROM app_tag WHERE lower(name) = lower(%s));'''
        now = datetime.datetime.now()
        parameters = ((tag, str(user), now, tag) for tag in tags)
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, parameters)
        finally:
            cursor.close()        
    
    @classmethod
    def get_tags(cls):
        return [tag for tag in cls.objects.filter(is_muted=False).order_by('name')]
    
    @staticmethod
    def clean_tags(tags):
        """
        Return cleaned tags string, removed spaces and special characters
        """
        tags = (re.sub(r'[^\w\.]', '', tag) for tag in tags) 
        tags = ','.join(tag for tag in tags if len(tag) > 1 and len(tag) <= 10)
        return tags

        
class FacebookUser(models.Model):
    """
    Facebook user information
    """
    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, unique=True)
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
   

