from rest_framework import serializers
from decimal import Decimal
from datetime import datetime
from .models import (
    User, Products, Banner, Carts, Receipt,
    Order, Category, Location, Table, TableBooking
)

# =========================
# BANNER
# =========================
class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ""


# =========================
# REGISTER
# =========================
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'password', 'confirm_password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create(**validated_data)


# =========================
# LOGIN (WORKING – DO NOT HASH)
# =========================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": "Email not found"})

        if user.password != data['password']:
            raise serializers.ValidationError({"errors": "Incorrect password"})

        return {
            "userId": user.userId,
            "name": user.name,
            "email": user.email,
        }


# =========================
# PRODUCT
# =========================
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ""


# =========================
# CART
# =========================
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = [
            'cartId',
            'userId',
            'productId',
            'name',
            'price',
            'qty',
            'img',
        ]


# =========================
# RECEIPT
# =========================
class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['receipt_number', 'subtotal', 'total_amount', 'created_at']


# =========================
# ORDER
# =========================
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# =========================
# CATEGORY
# =========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# =========================
# LOCATION
# =========================
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


# =========================
# TABLE
# =========================
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


# =========================
# TABLE BOOKING
# =========================
class TableBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableBooking
        fields = '__all__'
