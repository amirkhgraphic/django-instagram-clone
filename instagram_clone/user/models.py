import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from utils.utils import avatar_path


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address!'))

        email = self.normalize_email(email=email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=127, blank=False, null=False)
    last_name = models.CharField(max_length=127, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    about = models.TextField(_('About me'), max_length=500, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('user_name', 'first_name', 'last_name')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.user_name}"


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.user_name} is followed by {self.followed_by.user_name}"

    @staticmethod
    def followers_count(user):
        return Follower.objects.filter(user=user).all().count()

    @staticmethod
    def following_count(followed_by):
        return Follower.objects.filter(followed_by=followed_by).all().count()

    class Meta:
        unique_together = ('user', 'followed_by')