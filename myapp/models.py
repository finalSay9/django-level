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


    DEPARTMENT_CHOICES = [
        ('sciences', 'Sciences'),
        ('languages', 'Languages'),
        ('humanities', 'Humanities')
    ]


    CLASS_LEVEL = [
        ('form_1', 1),
        ('form_2', 2),
        ('form_3', 3),
        ('form_4', 4)
    ]

    SUBJECT = [
        ('english', 'English'),
        ('mathematics','Mathematics'),
        ('chemistry', 'Chemistry'),
        ('physics', 'Physics'),
        ('computer', 'Computer'),
        ('business', 'Business'),
    ]



    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    ]



    ROLE_CHOICES = [
        ('student',   'Student'),
        ('teacher',   'Teacher'),
        ('parent',    'Parent'),
        ('hr',        'HR'),
        ('bursar',    'Accountant'),
        ('head',    'Head'),
        
    ]
    
    # ── Fields that use choices ──────────────────────────────
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
    )

    primary_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        help_text="Main role — used for quick display & filtering",
    )

    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        blank=True,
        null=True,               # ← most students won't have department
        help_text="Main department (mainly for teachers)",
    )

    # Optional: if you want faster checks in code / templates
    @property
    def is_teacher(self):
        return self.primary_role == 'teacher'

    @property
    def is_student(self):
        return self.primary_role == 'student'

    USERNAME_FIELD = "email"                          # ← login with email, not username
    REQUIRED_FIELDS = []                              # fields asked when createsuperuser runs

    objects = CustomUserManager()

    def __str__(self):
        return self.email
