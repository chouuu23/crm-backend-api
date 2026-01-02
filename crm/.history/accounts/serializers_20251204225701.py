# accounts/serializers.py
from rest_framework import serializers
from .models import Student

class USerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'password']