# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'gender',
            'primary_role',      
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make password fields look nicer (optional)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        allowed_roles = [
            CustomUser.Role.STUDENT,
            CustomUser.Role.TEACHER,
            CustomUser.Role.PARENT,
        ]
        self.fields['primary_role'].choices = [
            (value, label) for value, label in CustomUser.Role.choices
            if value in allowed_roles
        ]