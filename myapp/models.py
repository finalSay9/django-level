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


#-----------------------------custom user--------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Authentication & core fields
    email = models.EmailField(unique=True, verbose_name="Email address")
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # ──────────────── Modern Choices ────────────────

    class Gender(models.TextChoices):
        MALE    = "M", "Male"
        FEMALE  = "F", "Female"
        OTHER   = "O", "Other / Prefer not to say"

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        PARENT  = "parent",  "Parent / Guardian"
        HR      = "hr",      "HR Staff"
        BURSAR  = "bursar",  "Bursar / Accountant"
        HEAD    = "head",    "Headteacher / Principal"

    class Department(models.TextChoices):
        SCIENCES   = "sciences",   "Sciences"
        LANGUAGES  = "languages",  "Languages"
        HUMANITIES = "humanities", "Humanities"
       
    class FormLevel(models.TextChoices):
        FORM_1 = "form_1", "Form 1"
        FORM_2 = "form_2", "Form 2"
        FORM_3 = "form_3", "Form 3"
        FORM_4 = "form_4", "Form 4"

    class Subject(models.TextChoices):
        ENGLISH    = "english",    "English"
        MATHEMATICS = "mathematics", "Mathematics"
        CHEMISTRY  = "chemistry",  "Chemistry"
        PHYSICS    = "physics",    "Physics"
        COMPUTER   = "computer",   "Computer Studies"
        BUSINESS   = "business",   "Business Studies"

    # ──────────────── Actual Model Fields ────────────────

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        verbose_name="Gender",
    )

    primary_role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,           
        verbose_name="Primary Role",
        help_text="Main role for display, quick filters, and basic access rules",
    )

    department = models.CharField(
        max_length=30,
        choices=Department.choices,
        blank=True,
        null=True,                      
        verbose_name="Department",
        help_text="Main teaching department (mostly for teachers)",
    )

   
    form_level = models.CharField(
        max_length=10,
        choices=FormLevel.choices,
        blank=True,
        null=True,
        verbose_name="Form Level",
        help_text="Only relevant for students",
    )

    # ──────────────── Meta & Helpers ────────────────

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [first_name]  

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


    @property
    def is_teacher(self):
        return self.primary_role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.primary_role == self.Role.STUDENT

    @property
    def is_headteacher(self):
        return self.primary_role == self.Role.HEAD



# ───── Role-specific profile models (OneToOne) ─────

class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
        limit_choices_to={'primary_role': CustomUser.Role.STUDENT},
    )
    
    # Student-specific fields
    admission_number = models.CharField(max_length=30, unique=True, blank=True)
    form_level = models.CharField(
        max_length=10,
        choices=[
            ('form_1', 'Form 1'),
            ('form_2', 'Form 2'),
            ('form_3', 'Form 3'),
            ('form_4', 'Form 4'),
        ],
        blank=True,
    )
    stream = models.CharField(max_length=2, blank=True)          
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)

    class Meta:
        verbose_name = "student profile"
        verbose_name_plural = "student profiles"

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        limit_choices_to={'primary_role': CustomUser.Role.TEACHER},
    )
    
    # Teacher-specific fields
    employee_id = models.CharField(max_length=30, unique=True, blank=True)
    department = models.CharField(
        max_length=30,
        choices=[
            ('sciences', 'Sciences'),
            ('languages', 'Languages'),
            ('humanities', 'Humanities'),
            ('technical', 'Technical / Vocational'),
        ],
        blank=True,
    )
    subjects_taught = models.ManyToManyField('Subject', blank=True, related_name='teachers') 
    hire_date = models.DateField(null=True, blank=True)
    qualifications = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='teachers/', blank=True, null=True)

    class Meta:
        verbose_name = "teacher profile"
        verbose_name_plural = "teacher profiles"

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"



#
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_code = models.CharField(max_length=10, blank=True)  
    department = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name