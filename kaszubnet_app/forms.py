from django import forms
from kaszubnet_app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wprowadź login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}))
