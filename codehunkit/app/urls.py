"""
Urls configuration for main app
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('codehunkit.app.views.home',
                       url(r'^$', 'index', name='app_home'),
                       url(r'^(?P<page_index>\d+)/$', 'index', name='app_home'),
                       url(r'^new/$', 'index', { 'sort_by_new': True }, name='app_home_new'),
                       url(r'^new/(?P<page_index>\d+)/$', 'index', { 'sort_by_new': True }, name='app_home_new'),
                       url(r'^tags/(?P<tag_name>[\w\.]+)/$', 'tag_snippets', name='app_tag'),
                       url(r'^tags/(?P<tag_name>[\w\.]+)/(?P<page_index>\d+)/$', 'tag_snippets', name='app_tag'),
                       url(r'^tags/(?P<tag_name>[\w\.]+)/new/$', 'tag_snippets', { 'sort_by_new': True }, name='app_tag_new'),
                       url(r'^tags/(?P<tag_name>[\w\.]+)/new/(?P<page_index>\d+)/$', 'tag_snippets', { 'sort_by_new': True }, name='app_tag_new'),
                       url(r'^search/$', 'search', name='app_search'),
                       url(r'^search/(?P<page_index>\d+)/$', 'search', name='app_search'),
                       url(r'^search/new/$', 'search', {'sort_by_new': True}, name='app_search_new'),
                       url(r'^search/new/(?P<page_index>\d+)/$', 'search', {'sort_by_new': True}, name='app_search_new'),
)

urlpatterns += patterns('codehunkit.app.views.languages',
                        url(r'^languages/(?P<slug>[\w-]+)/$', 'lang_snippets', name='app_lang'),
                        url(r'^languages/(?P<slug>[\w-]+)/(?P<page_index>\d+)/$', 'lang_snippets', name='app_lang'),
                        url(r'^languages/(?P<slug>[\w-]+)/new/$', 'lang_snippets', { 'sort_by_new': True }, name='app_lang_new'),
                        url(r'^languages/(?P<slug>[\w-]+)/new/(?P<page_index>\d+)/$', 'lang_snippets', { 'sort_by_new': True }, name='app_lang_new'),
                        url(r'^languages/(?P<slug>[\w-]+)/subscribe/$', 'lang_subscribe', name='app_lang_subscribe'),
                        url(r'^languages/(?P<slug>[\w-]+)/unsubscribe/$', 'lang_unsubscribe', name='app_lang_unsubscribe'),
)                  

urlpatterns += patterns('codehunkit.app.views.users',
                        url(r'^users/(?P<username>[\w\.]+)/$', 'user_snippets', name='app_user'),
                        url(r'^users/(?P<username>[\w\.]+)/(?P<page_index>\d+)/$', 'user_snippets', name='app_user'),
                        url(r'^users/(?P<username>[\w\.]+)/new/$', 'user_snippets', { 'sort_by_new':True }, name='app_user_new'),
                        url(r'^users/(?P<username>[\w\.]+)/new/(?P<page_index>\d+)/$', 'user_snippets', {'sort_by_new': True}, name='app_user_new'),
                        url(r'^users/(?P<username>[\w\.]+)/follow/$', 'user_follow', name='app_user_follow'),
                        url(r'^users/(?P<username>[\w\.]+)/unfollow/$', 'user_unfollow', name='app_user_unfollow'),
)

urlpatterns += patterns('codehunkit.app.views.badges',
                        url(r'^users/(?P<username>[\w\.]+)/badges/(?P<user_badge_id>\d+)/$', 'user_badge', name='app_user_badge'),
)

urlpatterns += patterns('codehunkit.app.views.snippets',
                        url(r'^snippets/create/$', 'snippet_create', name='app_snippet_create'),                        
                        url(r'^snippets/(?P<snippet_id>\d+)/$', 'snippet_read', name='app_snippet_read'),
                        url(r'^snippets/(?P<snippet_id>\d+)/(?P<slug>[\w-]+)/$', 'snippet_read', name='app_snippet_read'),
                        url(r'^snippets/(?P<snippet_id>\d+)/votes/up/$', 'snippet_vote', { 'action': 'UP' }, name='app_snippet_vote_up'),
                        url(r'^snippets/(?P<snippet_id>\d+)/votes/down/$', 'snippet_vote', { 'action': 'DOWN' }, name='app_snippet_vote_down'),
                        url(r'^snippets/(?P<snippet_id>\d+)/comments/create/$', 'comment_create', name='app_comment_create'),
                        url(r'^snippets/(?P<snippet_id>\d+)/comments/(?P<comment_id>\d+)/$', 'comment_read', name='app_comment_read'),
                        url(r'^snippets/(?P<snippet_id>\d+)/comments/(?P<comment_id>\d+)/replies/create/$', 'reply_create', name='app_reply_create'),
                        url(r'^snippets/(?P<snippet_id>\d+)/comments/(?P<comment_id>\d+)/votes/up/$', 'comment_vote', { 'action': 'UP' }, name='app_comment_vote_up'),
                        url(r'^snippets/(?P<snippet_id>\d+)/comments/(?P<comment_id>\d+)/votes/down/$', 'comment_vote', { 'action': 'DOWN' }, name='app_comment_vote_down'),
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

