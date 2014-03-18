"""
Forms
@author: faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

import re

from django import forms
from codehunkit.app.models import User, Language

class SignUp(forms.Form):
    """
    User registration form
    """
    username_regex = re.compile('^\w{4,30}$')
    username = forms.CharField(max_length=15, error_messages={'required': 'Please choose a username.'},
                               widget=forms.TextInput(attrs={'placeholder': 'Username...'}))
    email = forms.EmailField(error_messages={'required': 'Please enter your email address.'},
                             widget=forms.TextInput(attrs={'placeholder': 'Your e-mail address...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password...'}), min_length=8, error_messages={'required': 'Please enter your password for the website.'})
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=User.GENDERS, error_messages={'required': 'Please specify your gender.'})
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not self.username_regex.match(username):
            raise forms.ValidationError("Please choose an alphanumeric username of at least 4 characters and not more than 30 characters.")
        return username

class ChangePassword(forms.Form):
    """
    Change password form
    """
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your current password...'}), max_length=50, error_messages={'required': 'Please enter your current password.'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password...'}), min_length=8, max_length=50, error_messages={'required': 'Please enter your new password.'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password again...'}), max_length=50, error_messages={'required': 'Please re-enter your new password for confirmation.'})
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")        
        return confirm_password    


class SnippetForm(forms.Form):
    """
    Snippet submit form
    """
    gist_regex = re.compile(r'[^\w\.]+')
    gist = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Code description...'}),
                           error_messages={'required': 'Please write description of your code snippet'})
    code = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'cols': 1,
                                                                         'rows': 16,
                                                                         'style': 'width:100%;max-width:100%',
                                                                         'maxlength': '2000',
                                                                         'placeholder': 'Your code snippet here...'}),
                           error_messages={'required': 'Please write code you want to share'})    
    tags = forms.CharField(max_length=100, error_messages={'required': 'Choose some tags to for your code snippet'})
    
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        langs = [('', '')]
        langs += ((lang.id, lang.name,) for lang in Language.get_all())
        self.fields['language'] = forms.ChoiceField(choices=langs,  error_messages={'required': 'Select a language your of code snippet'})
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        return tags.strip(' ,')
    
    def clean_gist(self):
        gist = self.cleaned_data['gist']
        if len(self.gist_regex.split(gist)) < 4:
            raise forms.ValidationError("Please write few more words about your code snippet.")
        return gist
    
    def clean_code(self):
        code = self.cleaned_data['code']
        if len(code) < 20:
            raise  forms.ValidationError("Code snippet should be at least 20 characters.")
        return code
        
        

    
