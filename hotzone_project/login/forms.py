from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", 
        widget=forms.TextInput(attrs={'class': 'login-text-input'}), 
        required = True
    )

    password = forms.CharField(
        label='Password', 
        widget=forms.TextInput(attrs={'class': 'login-text-input'}), 
        required = True
    )