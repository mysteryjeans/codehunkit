"""
Django administration for CodeHunkit
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""


from codehunkit.app import models
from django.contrib import admin


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'description',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_on',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'


class LanguageGraphAdmin(admin.ModelAdmin):
    list_display = ('language', 'up_votes', 'down_votes', 'readers_count', 'coders_count', 'snippets_count')
    list_filter = ('updated_on',)
    search_fields = ('language',)
    date_hierarchy = 'updated_on'

    
class LanguageBadgeSummaryAdmin(admin.ModelAdmin):
    list_display = ('language', 'badge', 'badges_count',)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name', 'description',)    


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SchoolGraphAdmin(admin.ModelAdmin):
    list_display = ('school', 'up_votes', 'down_votes',  'coders_count',)


class SchoolBadgeSummaryAdmin(admin.ModelAdmin):
    list_display = ('school', 'badge', 'badges_count',)
    

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'gender',)
    list_filter = ('gender', 'created_on')
    

admin.site.register(models.Badge, BadgeAdmin)
admin.site.register(models.Language, LanguageAdmin)    
admin.site.register(models.LanguageGraph, LanguageGraphAdmin)
admin.site.register(models.LanguageBadgeSummary, LanguageBadgeSummaryAdmin)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.SchoolGraph, SchoolGraphAdmin)
admin.site.register(models.SchoolBadgeSummary, SchoolBadgeSummaryAdmin)
admin.site.register(models.User, UserAdmin)