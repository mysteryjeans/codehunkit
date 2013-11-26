"""
Authentication views
@author: Faraz Masood Khan faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import logging

from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from codehunkit.app import HunkitError
from codehunkit.app.views import render_response
from codehunkit.app.forms import ChangePassword, SignUp
from codehunkit.app.models import User
from codehunkit.app.decorators import anonymous_required


logger = logging.getLogger('django.request')


@anonymous_required
def login(request):
    """
    Login user using django builten authentication
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.has_activated:
                not_activated = True
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
                msg_text = get_template('app/email/activation.html').render(Context({ 'domain': domain, 'user': user }))
                msg = EmailMessage('codehunkit.com account activation', msg_text, 'CodeHunkit <noreply@codehunkit.com>', [user.email])
                msg.content_subtype = "html"
                msg.send()
                                
                msg_text = get_template('app/email/welcome.html').render(Context({ 'domain': domain, 'user': user }))
                msg = EmailMessage('codehunkit.com Welcome! Lets get started!!', msg_text, 'CodeHunkit <noreply@codehunkit.com>', [user.email])
                msg.content_subtype = "html"
                msg.send()
                successful_signup = True    
            except HunkitError as e:
                error = e.message
    else:
        form = SignUp()
    
    return render_response(request, 'app/public/signup.html', locals())


@anonymous_required
@transaction.commit_on_success
def facebook_login(request):
    """
    Login or sign up user via facebook
    """
    

@anonymous_required
def activation(request, user_id, code):
    """
    Activates the new user
    """
    if request.method == 'POST':
        raise Http404()
        
    try:
        user = User.objects.get(id=user_id)
        if not user.has_activated:            
            if user.activation_code == code:
                user.activate()        
            else:
                invalid_code = True
        else:
            error = 'Your account is already activated.'            
    except User.DoesNotExist:
        raise Http404()
    
    return render_response(request, 'app/public/activation.html', locals())


@anonymous_required
def send_activation(request, user_id):
    """
    Send activation code if user hasn't been activated yet
    """
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.has_activated:
            error = 'Your account is already activated.'
        else:
            msg_text = get_template('app/email/activation.html').render(Context({ 'domain': get_current_site(request).domain, 'user': user }))
            msg = EmailMessage('codehunkit.com account activation', msg_text, 'CodeHunkit <noreply@codehunkit.com>', [user.email])
            msg.content_subtype = "html"
            msg.send()        
        
        return render_response(request, 'app/public/send_activation.html', locals())

    return HttpResponseRedirect(reverse('app_home'))                
