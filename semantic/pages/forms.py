from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import EmailInput, PasswordInput

from core.models import User


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=EmailInput())
    password = forms.CharField(label='Пароль', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username')
