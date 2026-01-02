
from rest_framework import serializers
from .models import Users   # Change this to your actual model name (User or TblUsers)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userId', 'name', 'email', 'password']
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'productId',
            'categoryId',
            'name',
            'price',
            'image',
            'description',
            'rating',
            'isPopular',
        ]