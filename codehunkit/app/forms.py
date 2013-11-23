"""
Forms
@author: faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import re

from django import forms
from codehunkit.app.models import User

class SignUp(forms.Form):
    """
    User registration form
    """
    username_regex = re.compile('^\w{4,30}$')
    username = forms.CharField(max_length=15, error_messages={'required': 'Please choose a username.'})
    email = forms.EmailField(error_messages={'required': 'Please enter your email address.'})
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, error_messages={'required': 'Please enter your password for the website.'})
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=User.GENDERS, error_messages={'required': 'Please specify your gender.'})
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not self.username_regex.match(username):
            raise forms.ValidationError("Please choose an alphanumeric username of at least 4 characters and not more than 30 characters.")
        return username