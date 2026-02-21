# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile, TeacherProfile  


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = instance.primary_role

        if role == CustomUser.Role.STUDENT:
            StudentProfile.objects.create(user=instance)
            # You can set defaults or leave blank

        elif role == CustomUser.Role.TEACHER:
            TeacherProfile.objects.create(user=instance)

    