from rest_framework import serializers
from .models import CustomUser, StudentProfile, TeacherProfile, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'short_code','department']


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'primary_role', 'gender']
       

class StudentProfileSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    fields = [
            'id', 'user', 'form_level', 'stream',
            'guardian_name', 'guardian_phone', 'profile_picture'
        ]


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    subjects_taught = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'employee_id', 'department',
            'subjects_taught', 'hire_date', 'qualifications',
            'profile_picture'
        ]
