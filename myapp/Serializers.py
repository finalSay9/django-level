from rest_framework import serializers
from .models import CustomUser, StudentProfile, TeacherProfile, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
    



