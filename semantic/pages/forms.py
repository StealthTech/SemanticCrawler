import re

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import EmailInput, PasswordInput, Textarea
from django.core.files.images import get_image_dimensions

from core.models import User
from scanner.models import ScanRequest
from semantic.settings import AVATAR_MAX_HEIGHT, AVATAR_MAX_WIDTH


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=EmailInput())
    password = forms.CharField(label='Пароль', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username')


class SignUpForm(UserCreationForm):
    email = forms.CharField(label='Email', widget=EmailInput())
    nickname = forms.CharField(label='Никнейм')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password1 = forms.CharField(label='Пароль', widget=PasswordInput())
    password2 = forms.CharField(label='Пароль (ещё раз)', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'nickname', 'first_name', 'last_name', 'password1', 'password2')

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        nickname = nickname.strip()

        r = re.compile('^[A-Za-z0-9_]+$')
        if r.match(nickname) is None:
            raise forms.ValidationError('Ник может содержать только латинские буквы, цифры и знаки подчеркивания.')
        return nickname

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name = first_name.strip()

        r_rus = re.compile('^[А-Яа-я]+$')
        r_eng = re.compile('^[A-Za-z]+$')
        if r_rus.match(first_name) or r_eng.match(first_name):
            return first_name.capitalize()
        else:
            raise forms.ValidationError('Имя должно быть написано на латинице или кириллице.')

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name = last_name.strip()

        r_rus = re.compile('^[А-Яа-я]+$')
        r_eng = re.compile('^[A-Za-z]+$')
        if r_rus.match(last_name) or r_eng.match(last_name):
            return last_name.capitalize()
        else:
            raise forms.ValidationError('Фамилия должна быть написана на латинице или кириллице.')


class ProfileEditForm(ModelForm):
    avatar = forms.ImageField(label='Аватар участника', required=False)
    nickname = forms.CharField(label='Никнейм')
    email = forms.CharField(label='Электронная почта', disabled=True)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('avatar', 'nickname', 'email', 'first_name', 'last_name')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            w, h = get_image_dimensions(avatar)

            if w > AVATAR_MAX_WIDTH or h > AVATAR_MAX_HEIGHT:
                raise forms.ValidationError('Изображение должно иметь разрешение не более чем {}x{}.'.format(
                    AVATAR_MAX_WIDTH, AVATAR_MAX_HEIGHT))
        return avatar

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        nickname = nickname.strip()

        r = re.compile('^[A-Za-z0-9_]+$')
        if r.match(nickname) is None:
            raise forms.ValidationError('Ник может содержать только латинские буквы, цифры и знаки подчеркивания.')
        return nickname

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name = first_name.strip()

        r_rus = re.compile('^[А-Яа-яЁё]+$')
        r_eng = re.compile('^[A-Za-z]+$')
        if r_rus.match(first_name) or r_eng.match(first_name):
            return first_name.capitalize()
        else:
            raise forms.ValidationError('Имя должно быть написано на латинице или кириллице.')

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name = last_name.strip()

        r_rus = re.compile('^[А-Яа-яЁё]+$')
        r_eng = re.compile('^[A-Za-z]+$')
        if r_rus.match(last_name) or r_eng.match(last_name):
            return last_name.capitalize()
        else:
            raise forms.ValidationError('Фамилия должна быть написана на латинице или кириллице.')


class LaunchForm(ModelForm):
    url_list = forms.CharField(label='Список ссылок (через запятую)', widget=Textarea)

    class Meta:
        model = ScanRequest
        fields = ('url_list',)
