from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login")

        if user.password != data["password"]:
            raise serializers.ValidationError("Invalid login")

        return {
            "userId": user.userId,
            "name": user.name,
            "email": user.email,
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    tables_detail = TableSerializer(source="tables", many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"
