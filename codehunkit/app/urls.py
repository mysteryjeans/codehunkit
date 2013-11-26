"""
Urls configuration for main app
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('codehunkit.app.views',
                       url(r'^$', 'home', name='hunkit_home'),
                       url(r'^language/(?P<slug>[\w-]+)/$', 'lang_snippets', name='hunkit_lang'),
                       url(r'^language/(?P<slug>[\w-]+)/(?P<page_index>\d+)/$', 'lang_snippets', name='hunkit_lang'),
                       url(r'^language/(?P<slug>[\w-]+)/new/$', 'lang_snippets', { 'sort_by_new': True }, name='hunkit_lang_new'),
                       url(r'^language/(?P<slug>[\w-]+)/new/(?P<page_index>\d+)/$', 'lang_snippets', { 'sort_by_new': True }, name='hunkit_lang_new'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/$', 'tag_snippets', name='hunkit_tag'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/(?P<page_index>\d+)/$', 'tag_snippets', name='hunkit_tag'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/new/$', 'tag_snippets', { 'sort_by_new': True }, name='hunkit_tag_new'),
                       url(r'^tag/(?P<tag_name>[\w\.]+)/new/(?P<page_index>\d+)/$', 'tag_snippets', { 'sort_by_new': True }, name='hunkit_tag_new'),
                       url(r'^user/(?P<username>[\w\.]+)/$', 'user_snippets', name='hunkit_user'),
                       url(r'^user/(?P<username>[\w\.]+)/(?P<page_index>\d+)/$', 'user_snippets', name='hunkit_user'),
                       url(r'^user/(?P<username>[\w\.]+)/new/$', 'user_snippets', { 'sort_by_new':True }, name='hunkit_user_new'),
                       url(r'^user/(?P<username>[\w\.]+)/new/(?P<page_index>\d+)/$', 'user_snippets', {'sort_by_new': True}, name='hunkit_user_new'),
                       url(r'^search/$', 'search', name='hunkit_search'),
                       url(r'^search/(?P<page_index>\d+)/$', 'search', name='hunkit_search'),
                       url(r'^search/new/$', 'search', {'sort_by_new': True}, name='hunkit_search_new'),
                       url(r'^search/new/(?P<page_index>\d+)/$', 'search', {'sort_by_new': True}, name='hunkit_search_new'),
                       url(r'^snippet/create/$', 'create_snippet', name='hunkit_create_snippet'),    
                       url(r'^snippet/vote/$', 'snippet_vote', name='hunkit_snippet_vote'),
                       url(r'^login/$', 'login', name='hunkit_login'),
                       url(r'^logout/$', 'logout', name='hunkit_logout'),
                       url(r'^change_password/$', 'change_password', name='hunkit_change_password'),
                       url(r'^signup/$', 'sign_up', name='hunkit_sign_up'),
                       url(r'^activation/(?P<user_id>\d+)-(?P<code>\w+)/$', 'activation', name='hunkit_activation'),
                       url(r'^facebook_login/$', 'facebook_login', name='hunkit_facebook_login'),
                       url(r'^send_activation/(?P<user_id>\d+)/$', 'send_activation', name='hunkit_send_activation'),
)

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^forgot_password/$', 'password_reset',
                            {'template_name': 'app/public/forgot_password.html',
                             'email_template_name': 'app/email/password_reset.html',
                             'subject_template_name': 'app/email/password_reset_subject.txt',
                             'post_reset_redirect': '/forgot_password/done/'
                        }, name='hunkit_forgot_password'),
                        url(r'^forgot_password/done/$', 'password_reset_done', {'template_name': 'app/public/forgot_password_done.html'}, name='hunkit_forgot_password_done'),
                        url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'password_reset_confirm',
                            {'template_name': 'app/public/password_reset.html',
                             'post_reset_redirect': '/password_reset/done/' 
                        }, name='hunkit_password_reset'),
                        url(r'^password_reset/done/$', 'password_reset_complete', {'template_name': 'app/public/password_reset_done.html'}, name='hunkit_password_reset_done'),
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)

