from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class CustomuserManager(UserManager):
    def create_user(self, email, password=None, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(email=email, password=password, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email=email, password=password, is_staff=True,
                                is_superuser=True, permission=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    permission = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomuserManager()

    USERNAME_FIELD = 'email'
