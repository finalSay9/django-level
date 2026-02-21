# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile, TeacherProfile  # add others later


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = instance.primary_role

        if role == CustomUser.Role.STUDENT:
            StudentProfile.objects.create(user=instance)
            # You can set defaults or leave blank

        elif role == CustomUser.Role.TEACHER:
            TeacherProfile.objects.create(user=instance)

        # elif role == CustomUser.Role.PARENT:
        #     ParentProfile.objects.create(user=instance)
        # ... etc.

        # For HEAD, HR, BURSAR → usually created by admin → no auto-profile or different logic