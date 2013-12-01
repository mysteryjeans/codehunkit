"""
Core snippets models
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import re
import datetime

from django.db import models, connection
from django.db.models import F 
from django.template.defaultfilters import slugify

from codehunkit.db import models as db_models
from codehunkit.app.models.core import Language, LanguageGraph, User, UserGraph


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
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):        
        return self.gist
    
    @models.permalink
    def get_absolute_url(self):
        return ('app_snippet_read', (self.id, self.slug,))
    
    def tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
    
    @classmethod
    def read(cls, snippet_id, user, comment_id=None, max_comments=20):
        """
        Returns snippet with all it's comments sorted
        """
        result = list(cls.objects.raw('''
                                      SELECT s.*, l.name AS lang_name, l.slug AS lang_slug, u.username, v.index AS vote_index
                                      FROM app_snippet s                                      
                                      INNER JOIN app_user u ON s.user_id = u.id
                                      INNER JOIN app_language l ON s.language_id = l.id
                                      LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                                      WHERE s.id = %s
                                      ''', [user.id, snippet_id]))
        
        if len(result) == 0:
            raise cls.DoesNotExist
        
        snippet = result[0]
        
        if snippet.is_enabled and max_comments:
            if comment_id:            
                comments = list(Comment.objects.raw('''
                                                    SELECT c.*, v.index AS vote_index
                                                    FROM app_comment c
                                                    LEFT OUTER JOIN app_comment_vote v ON c.id = v.comment_id AND v.user_id = %s
                                                    WHERE c.snippet_id = %s AND c.comment_id >= %s 
                                                    ORDER BY c.rank DESC, c.id
                                                    LIMIT %s
                                                    ''', [user.id, snippet_id, comment_id, max_comments]))
            else:
                comments = list(Comment.objects.raw('''
                                                    SELECT c.*, v.index AS vote_index
                                                    FROM app_comment c
                                                    LEFT OUTER JOIN app_comment_vote v ON c.id = v.comment_id AND v.user_id = %s
                                                    WHERE c.snippet_id = %s
                                                    ORDER BY c.rank DESC, c.id
                                                    LIMIT %s
                                                    ''', [user.id, snippet_id, max_comments]))                   
            
            snippet.loaded_comments = comments
            if comment_id:
                snippet.comments = [comment for comment in comments if comment.comment_id == comment_id]
            else:
                snippet.comments = [comment for comment in comments if comment.reply_to_id == None]
            
            
            for comment in comments:
                comment.snippet = snippet
                comment.replies = [reply for reply in comments if reply.reply_to_id == comment.comment_id]
        
        return snippet
    
    @classmethod
    def get_snippets(cls, user, page_index, page_size, sort_by_new):
        """
        Returns all snippets
        """
        if sort_by_new:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.id DESC
                        LIMIT %s OFFSET %s
                        '''
        else:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.rank DESC, s.id DESC
                        LIMIT %s OFFSET %s
                        '''
            
        return [snippet for snippet in cls.objects.raw(sql_query, [user.id, page_size, page_index * page_size])]
    
    @classmethod
    def lang_snippets(cls, lang, user, page_index, page_size, sort_by_new):
        """
        Returns all snippets
        """
        if sort_by_new:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id AND l.id = %s
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.id DESC
                        LIMIT %s OFFSET %s
                        '''
        else:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id AND l.id = %s
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.rank DESC, s.id DESC
                        LIMIT %s OFFSET %s
                        '''
            
        return [snippet for snippet in cls.objects.raw(sql_query, [lang.id, user.id, page_size, page_index * page_size])]
    
    @classmethod
    def user_snippets(cls, user, app_user, page_index, page_size, sort_by_new):
        """
        Returns all snippets
        """
        if sort_by_new:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id AND u.id = %s
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.id DESC
                        LIMIT %s OFFSET %s
                        '''
        else:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id AND u.id = %s
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        ORDER BY s.rank DESC, s.id DESC
                        LIMIT %s OFFSET %s
                        '''
            
        return [snippet for snippet in cls.objects.raw(sql_query, [user.id, app_user.id, page_size, page_index * page_size])]

    @classmethod
    def tag_snippets(cls, tag_name, user, page_index, page_size, sort_by_new):
        """
        Returns all snippets
        """
        if sort_by_new:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        WHERE s.tags ILIKE %s
                        ORDER BY s.id DESC
                        LIMIT %s OFFSET %s
                        '''
        else:
            sql_query = '''
                        SELECT s.*, u.username, l.name AS lang_name, l.slug AS lang_slug, v.index AS vote_index
                        FROM app_snippet s
                        INNER JOIN app_user u ON s.user_id = u.id
                        INNER JOIN app_language l ON s.language_id = l.id
                        LEFT OUTER JOIN app_snippet_vote v ON s.id = v.snippet_id AND v.user_id = %s
                        WHERE s.tags ILIKE %s
                        ORDER BY s.rank DESC, s.id DESC
                        LIMIT %s OFFSET %s
                        '''
            
        return [snippet for snippet in cls.objects.raw(sql_query, [user.id, tag_name, page_size, page_index * page_size])]
    
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
                                     slug=slugify(gist[:50]),
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
        app_label = 'app'
        db_table = 'app_snippet_vote'
        unique_together = ('user', 'snippet')


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
    
    class Meta:
        app_label = 'app'
    
    def __unicode__(self):        
        return self.comment_text[:50] if self.comment_text else ''


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
        app_label = 'app'
        db_table = 'app_comment_vote'
        unique_together = ('user', 'comment')


class Tag(models.Model):    
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    is_muted = models.BooleanField(default=False)    
    is_default = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=75)

    class Meta:
        app_label = 'app'

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
        parameters = ((tag, str(user), now, tag) for tag in tags.split(','))
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
        