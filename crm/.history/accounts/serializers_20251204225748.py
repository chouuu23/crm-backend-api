
from rest_framework import serializers
from .models import User   # Change this to your actual model name (User or TblUsers)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
