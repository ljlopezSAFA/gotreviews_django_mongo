from django import forms
from django.contrib.auth.forms import AuthenticationForm
from gotreviews.models import *


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'mail', 'password')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")


