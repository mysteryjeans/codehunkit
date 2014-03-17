"""
Core models
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import random
import hashlib

from django.db import models
from django.db.models import F, Q 
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from codehunkit.db import models as db_models
from codehunkit.app import stats
from codehunkit.app import HunkitError


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
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
    
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
    readers_count = models.IntegerField(default=0)
    coders_count = models.IntegerField(default=0)
    snippets_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        db_table = 'app_language_graph'
    
    def __unicode__(self):
        return unicode(self.language)
    
    def guru_level(self):
        """
        Return guru level of code snippets submitted for this language
        """
        return int(stats.rating(self.up_votes, self.down_votes) * 100)


class Location(models.Model):
    """
    Location
    """
    name = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=50, blank=True, null=True)    
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_or_create(cls, name, username):
        """
        Create location if not already exists in database
        """
        name = name.strip()
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            return cls.objects.create(name=name, updated_by=username, created_by=username)


class School(models.Model):
    """
    School of users
    """
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_or_create(cls, name, username):
        """
        Create school if not already exists in database
        """
        name = name.strip()
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            school = cls.objects.create(name=name, slug=slugify(name), created_by=username)
            SchoolGraph.objects.create(school=school, updated_by=username)
            return school
            

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
        app_label = 'app'
        db_table = 'app_school_graph'
    
    def __unicode__(self):
        return unicode(self.school)
        
    def guru_level(self):
        """
        Return guru level of code snippets submitted by this University students
        """
        return int(stats.rating(self.up_votes, self.down_votes) * 100)
    

class User(AbstractUser):
    """
    Extended user more basic information
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = ((MALE, 'Male'),
               (FEMALE, 'Female'))
    
    birthday = models.DateField(null=True, blank=True)    
    gender = models.CharField(max_length=1, choices=GENDERS)
    hometown = models.ForeignKey(Location, null=True, related_name='hometown_users', blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    locale = models.CharField(max_length=10, blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)    
    verification_code = models.CharField(max_length=512, blank=True, null=True)
    fb_account = models.BooleanField(default=False)   
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = [ 'email', 'updated_by', 'created_by', 'is_verified']
    
    class Meta:
        app_label = 'app'
    
    def get_langs(self):
        """
        Returns list of user's followed languages
        """
        return Subscription.get_langs(self)        
        
    def get_followings(self):
        """
        Users that this user is followings
        """
        return Follow.get_followings(self) 
    
    def verify(self):
        """
        Verify user account if not verified
        """
        User.objects.filter(id=self.id, is_verified=False).update(is_verified=True, updated_by=str(self))
                
    def change_password(self, password, new_password):        
        """
        Change user's password
        """
        if not self.check_password(password):            
            raise HunkitError('Wrong password! please enter your current password again.')
        
        self.set_password(new_password)
    
    def get_badges(self):
        """
        Returns list of user's earned badges
        """
        from badges import UserBadge
        return UserBadge.get_badges(self)
        
    @classmethod 
    def sign_up(cls, username, email, password, gender, hometown=None, location=None, locale=None, fb_account=False, is_verified=False):
        """
        Creates a new non-admin user in database 
        """
        from badges import Badge, UserBadge
               
        try:
            user = cls.objects.get(Q(username=username) | Q(email=email))
            if user.username == username:
                raise HunkitError('Username "%s" already registered with us, if you forgotten your password? <a href="%s">Request new one</a> or choose a different username.' % (username, reverse('app_forgot_password')))
            
            raise HunkitError('Its seems to be that you are already registered with this email address, if you forgotten your password? <a href="%s">Request new one.</a>' % reverse('app_forgot_password'))            
        except cls.DoesNotExist:
                        
            verification_code = None
            if not is_verified:
                verification_code = _random_digest()
            
            if hometown:
                hometown = Location.get_or_create(hometown, username)
            
            if location:
                location = Location.get_or_create(location, username)
                
            user = cls.objects.create_user(username=username,
                                           email=email,
                                           password=password,
                                           gender= gender,
                                           hometown=hometown,
                                           location=location,
                                           locale=locale,
                                           is_verified=is_verified,
                                           verification_code=verification_code,
                                           updated_by=username,
                                           created_by=username)
            
            UserGraph.objects.create(user=user, created_by=username)
            
            # Create subscriptions to default languages
            langs = []
            for lang in Language.objects.filter(is_default=True):
                langs.append(lang.id)
                Subscription.objects.create(user=user,language=lang, created_by=username)
            
            if langs:
                LanguageGraph.objects.filter(language_id__in=langs).update(readers_count=F('readers_count') + 1)
                
            # Awarding Freshman badge
            UserBadge.award(user, Badge.get_freshman())
                
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
        app_label = 'app'
        db_table = 'app_user_graph'
    
    def __unicode__(self):
        return unicode(self.user)
    
    def guru_score(self):
        """
        Return expertness of User on coding based
        """
        return int(stats.rating(self.up_votes, self.down_votes) * 100)


class Education(models.Model):
    """
    User education
    """
    user = models.ForeignKey(User)
    school = models.ForeignKey(School)
    degree = models.CharField(max_length=250, null=True)
    year = models.IntegerField(null=True)
    type = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        unique_together = ('user', 'school', 'degree', 'year', 'type')
    
    def __unicode__(self):
        return u'%s - %s - %s' % (self.degree, self.year, self.school)


class Subscription(models.Model):
    """
    User subscription for languages
    """
    user = models.ForeignKey(User)
    language = models.ForeignKey(Language)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        unique_together = ('user', 'language')
    
    def __unicode__(self):
        return unicode(self.language)
    
    @classmethod
    def get_langs(cls, user):
        """
        Return list of subscribed languages by user
        """
        return list(Language.objects.filter(subscription__user=user))
        
    @classmethod
    def is_subscribed(cls, lang, user):
        """
        Determine if user is following 
        """
        return cls.objects.filter(language=lang, user=user).exists()
    
    @classmethod
    def subscribe(cls, lang, user):        
        if not cls.objects.filter(language=lang, user=user).exists():
            cls.objects.create(language=lang,user=user, created_by=unicode(user))
            LanguageGraph.objects.filter(language=lang).update(readers_count=F('readers_count') + 1)
    
    @classmethod
    def unsubscribe(cls, lang, user):
        try:            
            subscription = cls.objects.get(language=lang, user=user)
            subscription.delete()
            LanguageGraph.objects.filter(language=lang).update(readers_count=F('readers_count') - 1)
        except cls.DoesNotExist:
            pass  


class Follow(models.Model):
    """
    User following class
    """
    id = db_models.BigAutoField(primary_key=True)
    follower = models.ForeignKey(User, related_name='followings') # user.followings will list users he followed
    following = models.ForeignKey(User, related_name='followers') # user.followers will list users following him 
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        unique_together = ('follower', 'following')
    
    @classmethod
    def get_followings(cls, user):
        """
        Returns list of users followed by this user
        """
        return [user for user in User.objects.raw('''
                                                  SELECT u.*, fb.id AS fb_id
                                                  FROM app_user u
                                                  INNER JOIN app_follow f ON u.id = f.following_id AND f.follower_id = %s
                                                  LEFT OUTER JOIN app_facebookuser fb ON u.id = fb.user_id
                                                  ORDER BY f.id
                                                  ''', [user.id])]
        
    
    @classmethod
    def is_follower(cls, following, follower):
        """
        Determine if user is following 
        """
        return cls.objects.filter(following=following, follower=follower).exists()
    
    @classmethod
    def follow(cls, following, follower):
        """
        Start following user
        """        
        if not cls.objects.filter(following=following, follower=follower).exists() and following.id != follower.id:
            cls.objects.create(following=following, follower=follower, created_by=unicode(follower))
            UserGraph.objects.filter(user=following).update(followers_count=F('followers_count') + 1)
    
    @classmethod
    def unfollow(cls, following, follower):
        """
        Unfollow the user
        """
        try:            
            follow = cls.objects.get(following=following, follower=follower)
            follow.delete()
            UserGraph.objects.filter(user=following).update(followers_count=F('followers_count') - 1)
        except cls.DoesNotExist:
            pass   
     
        
class FacebookUser(models.Model):
    """
    Facebook user information
    """
    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    access_token = models.CharField(max_length=2048,blank=True,null=True) # Sizes can grow and shrink therefore 2K should be enough
    access_expiry = models.DateTimeField(blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=75)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=75)
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):
        return self.username
    
    @classmethod
    def connect_user(cls, user, fb_user, access_token, access_expiry):
        """
        Associate Facebook user with Codehunkit user, not already exists and return True, user
        """
        fb_id = fb_user['id']
        fb_username = fb_user['username']
        try:
            fb_user = cls.objects.select_related('user').get(id=fb_id)
            if fb_user.user_id != user.id:
                raise HunkitError("Facebook account '%s' is already connected with a different Codehunkit user" % fb_username)
            fb_user.access_token = access_token
            fb_user.access_expiry = access_expiry
            fb_user.save()
            return False
        except cls.DoesNotExist: 
            name = fb_user['name']
            gender = User.MALE if fb_user['gender'] == 'male' else User.FEMALE
            email = fb_user['email']
            hometown = fb_user['hometown']['name'] if 'hometown' in fb_user else None
            location = fb_user['location']['name'] if 'location' in fb_user else None
            locale = fb_user['locale'] if 'locale' in fb_user else None
               
            user = User.objects.get(id=user.id)
            if user.gender is None: user.gender = gender
            if user.hometown is None: user.hometown = Location.get_or_create(hometown, user.username)
            if user.location is None: user.location = Location.get_or_create(location, user.username)
            if user.locale is None: user.locale = locale
            user.fb_account = True
            user.save()
            
            if 'education' in fb_user:
                for education in fb_user['education']:
                    if 'school' in education:
                        school = School.get_or_create(education['school']['name'], user.username)
                        degree = education['degree']['name'] if 'degree' in education else None
                        year = int(education['year']['name']) if 'year' in education else None
                        edu_type = education.get('type', None)
                        if not Education.objects.filter(school=school, user=user, degree=degree, year=year, type=edu_type).exists():
                            Education.objects.create(user=user, school=school, degree=degree, year=year, type=edu_type, updated_by=str(user), created_by=str(user))
                        
            cls.objects.create(user=user,
                               id=fb_id,
                               name=name,
                               username=fb_username,
                               email=email,
                               access_token=access_token,
                               access_expiry=access_expiry)                
            return True
    
    @classmethod
    def get_user_or_create(cls, fb_user, access_token, access_expiry):
        """
        Returns Codehunkit user associated with Facebook user or creates a new Codehunkit user
        """
        fb_id = fb_user['id']
        try:
            fb_user = cls.objects.select_related('user').get(id=fb_id)
            fb_user.access_token = access_token
            fb_user.access_expiry = access_expiry
            fb_user.save()
            return False, fb_user.user
        except cls.DoesNotExist:
            name = fb_user['name']
            fb_username = fb_user['username']
            # Checking for username in database
            username =  'fb_' + fb_username if User.objects.filter(username__iexact=fb_username).exists() else fb_username
            gender = User.MALE if fb_user['gender'] == 'male' else User.FEMALE
            email = fb_user['email']
            hometown = fb_user['hometown']['name'] if 'hometown' in fb_user else None
            location = fb_user['location']['name'] if 'location' in fb_user else None
            locale = fb_user['locale'] if 'locale' in fb_user else None
            verified = fb_user['verified']
            
            # Setting random password, since user will use Facebook to login otherwise he can recover his password
            user = User.sign_up(username, email, _random_digest(), gender, hometown, location, locale, True, verified)
            
            if 'education' in fb_user:
                for education in fb_user['education']:
                    if 'school' in education:
                        degree = education['degree']['name'] if 'degree' in education else None
                        year = int(education['year']['name']) if 'year' in education else None
                        edu_type = education.get('type', None)
                        school = School.get_or_create(education['school']['name'], username)
                        Education.objects.create(user=user, school=school, degree=degree, year=year, type=edu_type, updated_by=username, created_by=username)
            
            cls.objects.create(user=user,
                               id=fb_id,
                               name=name,
                               username=fb_username,
                               email=email,
                               access_token=access_token,
                               access_expiry=access_expiry)            
            
            return True, user
    
    
def _random_digest():
    algo = hashlib.md5()
    algo.update(str(random.randrange(100, 10000000)))
    return algo.hexdigest()
