from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('users must have email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email =models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)     # ← can access admin?
    date_joined = models.DateTimeField(auto_now_add=True)

    ROLE_CHOICES = [
        ('student',   'Student'),
        ('teacher',   'Teacher'),
        ('parent',    'Parent'),
        ('hr',        'HR'),
        ('bursar',    'Accountant'),
        ('head',    'Head'),
        
    ]
    primary_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        help_text="Main role — mainly for display & quick filters"
    )

    def __str__(self):
        return self.get_full_name() or self.username or self.email


    USERNAME_FIELD = "email"                          # ← login with email, not username
    REQUIRED_FIELDS = []                              # fields asked when createsuperuser runs

    objects = CustomUserManager()

    def __str__(self):
        return self.email
