"""
Urls configuration for main app
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('codehunkit.app.views',
    url(r'^$', 'home', name='app_home'),
    url(r'^login/$', 'login', name='app_login'),
    url(r'^logout/$', 'logout', name='app_logout'),
    url(r'^signup/$', 'sign_up', name='app_sign_up'),
    url(r'^activation/(?P<user_id>\d+)-(?P<code>\w+)/$', 'activation', name='app_activation'),
    url(r'^facebook_login/$', 'facebook_login', name='app_facebook_login'),
    url(r'^send_activation/(?P<user_id>\d+)/$', 'send_activation', name='app_send_activation'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^forgot_password/$', 'password_reset',
        {'template_name': 'app/public/forgot_password.html',
         'email_template_name': 'app/email/password_reset.html',
         'subject_template_name': 'app/email/password_reset_subject.txt',
         'post_reset_redirect': '/forgot_password/done/'
    }, name='app_forgot_password'),
    url(r'^forgot_password/done/$', 'password_reset_done', {'template_name': 'app/public/forgot_password_done.html'}, name='app_forgot_password_done'),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'password_reset_confirm',
        {'template_name': 'app/public/password_reset.html',
         'post_reset_redirect': '/password_reset/done/' 
    }, name='app_password_reset'),
    url(r'^password_reset/done/$', 'password_reset_complete', {'template_name': 'app/public/password_reset_done.html'}, name='app_password_reset_done'),
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)

