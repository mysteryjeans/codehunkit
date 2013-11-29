"""
Urls configuration for main app
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('codehunkit.app.views.snippets',
                       url(r'^$', 'home', name='app_home'),
                       url(r'^(?P<page_index>\d+)/$', 'home', name='app_home'),
                       url(r'^new/$', 'home', { 'sort_by_new': True }, name='app_home_new'),
                       url(r'^new/(?P<page_index>\d+)/$', 'home', { 'sort_by_new': True }, name='app_home_new'),
                       url(r'^language/(?P<slug>[\w-]+)/$', 'lang_snippets', name='app_lang'),
                       url(r'^language/(?P<slug>[\w-]+)/(?P<page_index>\d+)/$', 'lang_snippets', name='app_lang'),
                       url(r'^language/(?P<slug>[\w-]+)/new/$', 'lang_snippets', { 'sort_by_new': True }, name='app_lang_new'),
                       url(r'^language/(?P<slug>[\w-]+)/new/(?P<page_index>\d+)/$', 'lang_snippets', { 'sort_by_new': True }, name='app_lang_new'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/$', 'tag_snippets', name='app_tag'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/(?P<page_index>\d+)/$', 'tag_snippets', name='app_tag'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/new/$', 'tag_snippets', { 'sort_by_new': True }, name='app_tag_new'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/new/(?P<page_index>\d+)/$', 'tag_snippets', { 'sort_by_new': True }, name='app_tag_new'),
                       url(r'^user/(?P<username>[\w\.]+)/$', 'user_snippets', name='app_user'),
                       url(r'^user/(?P<username>[\w\.]+)/(?P<page_index>\d+)/$', 'user_snippets', name='app_user'),
                       url(r'^user/(?P<username>[\w\.]+)/new/$', 'user_snippets', { 'sort_by_new':True }, name='app_user_new'),
                       url(r'^user/(?P<username>[\w\.]+)/new/(?P<page_index>\d+)/$', 'user_snippets', {'sort_by_new': True}, name='app_user_new'),
                       url(r'^search/$', 'search', name='app_search'),
                       url(r'^search/(?P<page_index>\d+)/$', 'search', name='app_search'),
                       url(r'^search/new/$', 'search', {'sort_by_new': True}, name='app_search_new'),
                       url(r'^search/new/(?P<page_index>\d+)/$', 'search', {'sort_by_new': True}, name='app_search_new'),
)

urlpatterns += patterns('codehunkit.app.views.snippet',
                        url(r'^snippet/create/$', 'snippet_create', name='app_snippet_create'),
                        url(r'^snippet/vote/$', 'snippet_vote', name='app_snippet_vote'),
                        url(r'^snippet/(?P<snippet_id>\d+)/(?P<slug>[\w-]+)/$', 'snippet_read', name='app_snippet_read'),
                        url(r'^comment/create/$', 'comment_create', name='app_comment_create'),
                        url(r'^comment/vote/$', 'comment_vote', name='app_comment_vote'),
)

urlpatterns += patterns('codehunkit.app.views.auth',
                        url(r'^login/$', 'login', name='app_login'),
                        url(r'^logout/$', 'logout', name='app_logout'),
                        url(r'^change_password/$', 'change_password', name='app_change_password'),
                        url(r'^signup/$', 'sign_up', name='app_sign_up'),
                        url(r'^activation/(?P<user_id>\d+)-(?P<code>\w+)/$', 'activation', name='app_activation'),
                        url(r'^facebook_login/$', 'facebook_login', name='app_facebook_login'),
                        url(r'^send_activation/(?P<user_id>\d+)/$', 'send_activation', name='app_send_activation'),
)

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^forgot_password/$', 'password_reset', {'template_name': 'app/public/forgot_password.html',
                                                                      'email_template_name': 'app/email/password_reset.html',
                                                                      'subject_template_name': 'app/email/password_reset_subject.txt',
                                                                      'post_reset_redirect': '/forgot_password/done/'
                        }, name='app_forgot_password'),
                        url(r'^forgot_password/done/$', 'password_reset_done', {'template_name': 'app/public/forgot_password_done.html'}, name='app_forgot_password_done'),
                        url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                            'password_reset_confirm', {'template_name': 'app/public/password_reset.html',
                                                       'post_reset_redirect': '/password_reset/done/' 
                        }, name='app_password_reset'),
                        url(r'^password_reset/done/$', 'password_reset_complete', {'template_name': 'app/public/password_reset_done.html'}, name='app_password_reset_done'),
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)

