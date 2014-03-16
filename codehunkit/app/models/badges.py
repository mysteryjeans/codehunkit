"""
Rewards for user activties
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

from django.db import models
from django.db.models import F

from codehunkit.app.models.core import Language, School, User

class Badge(models.Model):
    """
    User's badges based on expertness
    """    
    name = models.CharField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    description = models.TextField()
    awarded_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):
        return self.name


class LanguageBadgeSummary(models.Model):
    """
    Summary of badges earn by language
    """
    language = models.ForeignKey(Language)
    badge = models.ForeignKey(Badge)
    awarded_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        db_table = 'app_language_badge_summary'


class UserBadge(models.Model):
    """
    Badge earn by user
    """
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        db_table = 'app_user_badge'
        unique_together = ('user', 'badge',)

    def __unicode__(self):
        return unicode(self.badge)

    @models.permalink
    def get_absolute_url(self):
        return ('app_user_badge', (self.user.username, self.id,))
    
    @classmethod
    def get_badges(cls, user, max_badges=0):
        query = cls.objects.select_related('user', 'badge').filter(user=user)
        return list(query[:max_badges] if max_badges else query)
    
    @classmethod
    def award(cls, user, badge):
        cls.objects.create(user=user, badge=badge, created_by=unicode(user))
        Badge.objects.filter(id=badge.id).update(awarded_count=F('awarded_count') + 1)


class SchoolBadgeSummary(models.Model):
    """
    Summary for badge earn by school students
    """
    school = models.ForeignKey(School)
    badge = models.ForeignKey(Badge)
    awarded_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'app'
        db_table = 'app_school_badge_summary'
        unique_together = ('school', 'badge',) 


FreshmanBadge = Badge.objects.get(name__iexact='Freshman')
VoterBadge = Badge.objects.get(name__iexact='Voter')
CommentatorBadge = Badge.objects.get(name__iexact='Commentator')
ContributorBadge = Badge.objects.get(name__iexact='Contributor')