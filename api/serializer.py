from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','password')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        # fields = ['full_name','address','job','phone_number','summary','age','country','freelancer','image','banner']
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'required': False}
        }

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'required': False}
        }

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'required': False}
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'required': False}
        }

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'required': False}
        }