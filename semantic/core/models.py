from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', unique=True)
    nickname = models.CharField(verbose_name='никнейм', max_length=32, unique=True)
    first_name = models.CharField(verbose_name='имя', max_length=32)
    last_name = models.CharField(verbose_name='фамилия', max_length=32)

    email_verified = models.BooleanField(verbose_name='email подтверждён', blank=True, default=False)
    date_joined = models.DateTimeField(verbose_name='дата подключения', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='активен', default=True)
    is_staff = models.BooleanField(verbose_name='сотрудник', default=False)

    avatar = models.ImageField(verbose_name='avatar', upload_to='users/avatars/', null=True, blank=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('profile', args={'nickname': self.nickname})
