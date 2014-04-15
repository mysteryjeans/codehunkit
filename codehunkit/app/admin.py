"""
Django administration for Codehunkit
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""


from codehunkit.app import models
from django.contrib import admin

class ModelAdmin(admin.ModelAdmin):
    """
    Abstract admin models for populating columns updated_by and created_by
    """
    exclude = ('updated_by', 'created_by',)
    def save_form(self, request, form, change):
        obj = super(ModelAdmin, self).save_form(request, form, change)
        
        if hasattr(obj, 'updated_by'):
            obj.updated_by = unicode(request.user)
       
        if hasattr(obj, 'created_by') and not obj.created_by:
            obj.created_by = unicode(request.user)
            
        return obj    

class LanguageAdmin(ModelAdmin):
    list_display = ('name', 'website', 'description',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_on',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'


class LanguageGraphAdmin(ModelAdmin):
    list_display = ('language', 'up_votes', 'down_votes', 'readers_count', 'coders_count', 'snippets_count')
    list_filter = ('updated_on',)
    search_fields = ('language',)
    date_hierarchy = 'updated_on'

    
class LanguageBadgeSummaryAdmin(ModelAdmin):
    list_display = ('language', 'badge', 'awarded_count',)


class BadgeAdmin(ModelAdmin):
    list_display = ('name', 'group_name', 'description',)    


class SchoolAdmin(ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SchoolGraphAdmin(ModelAdmin):
    list_display = ('school', 'up_votes', 'down_votes',  'coders_count',)


class SchoolBadgeSummaryAdmin(ModelAdmin):
    list_display = ('school', 'badge', 'awarded_count',)
    

class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'gender',)
    list_filter = ('gender', 'created_on')


class SnippetAdmin(ModelAdmin):
    list_display = ('id', 'gist', 'user', 'language', 'votes', 'rank', 'comments_count', 'created_on',)
    date_hierarchy = 'created_on'


class CommentAdmin(ModelAdmin):
    list_display = ('id', 'user', 'comment_text', 'votes', 'created_on',)
    date_hierarchy = 'created_on'


admin.site.register(models.Badge, BadgeAdmin)
admin.site.register(models.Language, LanguageAdmin)    
admin.site.register(models.LanguageGraph, LanguageGraphAdmin)
admin.site.register(models.LanguageBadgeSummary, LanguageBadgeSummaryAdmin)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.SchoolGraph, SchoolGraphAdmin)
admin.site.register(models.SchoolBadgeSummary, SchoolBadgeSummaryAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Snippet, SnippetAdmin)
admin.site.register(models.Comment, CommentAdmin)