"""
Authentication views
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import json
import urllib
import logging
import datetime
import urlparse

from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from codehunkit.app import HunkitError, scraper
from codehunkit.app.views import render_response
from codehunkit.app.forms import ChangePassword, SignUp
from codehunkit.app.models import User, FacebookUser, FlashMessage
from codehunkit.app.decorators import anonymous_required


logger = logging.getLogger('django.request')


@anonymous_required
def login(request):
    """
    Login user using django builten authentication
    """
    next_url = request.GET.get('next', None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_verified:
                is_verified = True
            elif user.is_active:
                login_user(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('app_home')))
            else:
                error = '''Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:hi@codehunkit.com">support</a>.''' 
        else:
            error = '''Username and password didn't matched, if you forgot your password? <a href="%s">Request new one</a>''' % reverse('app_forgot_password')
    
    return render_response(request, 'app/public/login.html', locals()) 


def logout(request):
    """
    Logout the user and flush his session data
    """
    logout_user(request)
    return HttpResponseRedirect(reverse('app_home'))
        

@login_required
def change_password(request):
    """
    Updates user's password in database
    """
    error = None
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:                
                request.user.change_password(data['current_password'], data['password'])
                successfully_changed = True
            except HunkitError as e:
                error = e.message
    else:
        form = ChangePassword()
    
    return render_response(request, 'app/change_password.html', locals())


@anonymous_required
@transaction.commit_on_success
def sign_up(request):
    """
    Create a new user account
    """
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.sign_up(data['username'], data['email'], data['password'], data['gender'])

                domain = get_current_site(request).domain
                _send_verification_email(domain, user)
                _send_welcome_email(domain, user)
                
                successful_signup = True    
            except HunkitError as e:
                error = e.message
    else:
        form = SignUp()
    
    return render_response(request, 'app/public/signup.html', locals())


@transaction.commit_on_success
def fb_login(request):
    """
    Login or sign up user via facebook
    """
    if request.method == 'POST':
        params = urllib.urlencode({'client_id': settings.FB_APP_ID,
                                   'response_type': 'code',
                                   'redirect_uri': request.build_absolute_uri(request.path),
                                   'state': request.POST.get('next', reverse('app_home')), # redirect uri for user
                                   'scope': 'email'
                                   })
        
        return HttpResponseRedirect(settings.FB_AUTH_URL + '?' + params)
    
    code = request.GET.get('code', None)
    next_url = request.GET.get('state', None)
    if not next_url: next_url = reverse('app_home')
    
    if not code:
        error = request.GET.get('error', None)
        error_reason = request.GET.get('error_reason', None)
        if error == 'access_denied' and error_reason == 'user_denied':
            return render_response(request, 'app/public/facebook_login.html', {'error': 'You must allow Codehunkit to access your basic information from Facebook.', 'next_url': next_url })
            
        logger.error('Error occurred while signing user through Facebook.\n' + str(request))    
        return render_response(request, 'app/public/facebook_login.html', {'error': 'We encounter some error while logging you in through Facebook.', 'next_url': next_url })
            
    params = urllib.urlencode({'client_id': settings.FB_APP_ID, 
                               'client_secret': settings.FB_APP_SECRET,
                               'redirect_uri': request.build_absolute_uri(request.path),
                               'code': code })
    
    try:        
        access_content = scraper.get_content(settings.FB_ACCESS_TOKEN + '?' + params)    
        access_content = dict(urlparse.parse_qsl(access_content))
        access_token = access_content['access_token']
        access_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(access_content['expires']))
        request.session['facebook_access_token'] = access_token
        params = urllib.urlencode({'access_token': access_token})
        
        fb_user = scraper.get_content(settings.FB_GRAPH_ME + '?' + params)
        fb_user = json.loads(fb_user)
        try:
            if request.user.is_authenticated():
                user = request.user
                created = FacebookUser.connect_user(user, fb_user, access_token, access_expiry)
                if created:
                    FlashMessage.add_success('Your Facebook account is successfully connected.', user)
            else:
                if not 'email' in fb_user:
                    raise HunkitError('You need to allow Codehunkit for access of your email address on Facebook')
                created, user = FacebookUser.get_user_or_create(fb_user, access_token, access_expiry)
                if not user.is_active:
                    raise HunkitError('Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:hi@codehunkit.com">support</a>.')

                if created:
                    domain = get_current_site(request).domain
                    
                    if user.is_verified:
                        user.backend='django.contrib.auth.backends.ModelBackend' # can't call authenticate since don't know password
                        login_user(request, user)
                        FlashMessage.add_success('You have successfully signed up with Facebook account.', user)
                    else:               
                        _send_verification_email(domain, user)
                        FlashMessage.add_success('You have successfully signed up with Facebook account, but you need to verify your account via email address.', user)
                        
                    _send_welcome_email(domain, user)                   
                else:
                    if user.is_verified:
                        user.backend='django.contrib.auth.backends.ModelBackend' # can't call authenticate since don't know password
                        login_user(request, user)
                        FlashMessage.add_info('Welcome back, ' + user.username + '!', user)
                    else:
                        return HttpResponseRedirect(reverse('app_send_verification'))
                 

            #if created:        
                #return HttpResponseRedirect(reverse('app_user_friends', args=[user.username]) + '?' + urllib.urlencode({ 'next': return_url}))        
            
            return HttpResponseRedirect(next_url)            
        except HunkitError as e:
            transaction.rollback()
            return render_response(request, 'app/public/facebook_login.html', {'error': e.message, 'next_url': next_url })
    except Exception as e:
        logger.exception(e)
        transaction.rollback()
        return render_response(request, 'app/public/facebook_login.html', {'error': 'We encounter some error while logging you in through Facebook.', 'next_url': next_url })
    
    return HttpResponseRedirect(reverse('app_home'))
    

@anonymous_required
def verification(request, user_id, code):
    """
    Activates the new user
    """
    if request.method == 'POST':
        raise Http404()
        
    try:
        user = User.objects.get(id=user_id)
        if not user.is_verified:            
            if user.verification_code == code:
                user.verify()        
            else:
                invalid_code = True
        else:
            error = 'Your account is already verified.'            
    except User.DoesNotExist:
        raise Http404()
    
    return render_response(request, 'app/public/verification.html', locals())


@anonymous_required
def send_verification(request, user_id):
    """
    Send verification code if user hasn't been verified yet
    """
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_verified:
            error = 'Your account is already verified.'
        else:
            _send_verification_email(get_current_site(request).domain, user)
            message = 'An account verification code has been sent to your email address'
        
    return render_response(request, 'app/public/send_verification.html', locals())


def _send_verification_email(domain, user):   
    msg_text = get_template('app/email/verification.html').render(Context({ 'domain': domain, 'user': user }))
    msg = EmailMessage('codehunkit.com account verification', msg_text, 'Codehunkit <noreply@codehunkit.com>', [user.email])
    msg.content_subtype = "html"
    msg.send()
    

def _send_welcome_email(domain, user):                                
    msg_text = get_template('app/email/welcome.html').render(Context({ 'domain': domain, 'user': user }))
    msg = EmailMessage('codehunkit.com Welcome! Lets get started!!', msg_text, 'Codehunkit <noreply@codehunkit.com>', [user.email])
    msg.content_subtype = "html"
    msg.send()          
