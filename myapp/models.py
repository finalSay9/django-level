from django.db import models
from django.contrib.auth.model import AbstractBaseUser, BaseUserManager, PermissionMixins


class CreateCustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('users must have email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        

