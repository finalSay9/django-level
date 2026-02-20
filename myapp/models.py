from django.db import models
from django.contrib.auth.model import AbstractBaseUser, BaseUserManager, PermissionMixins


class CreateCustomUserManager(BaseUserManager):
    
