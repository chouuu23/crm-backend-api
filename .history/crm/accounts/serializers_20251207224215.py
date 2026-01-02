from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User,Products, SlideShow, Carts, Receipt, Order,Category
# Imports Users, Products, TblSlideShow, TblCarts, TblReceipt


# ------------------------ USER ------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
# ------------------------ REGISTER ------------------------

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove unused field
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

# ------------------------ PRODUCT ------------------------
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return ""


# ------------------------ SLIDE SHOW ------------------------
class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = [
            'ID',
            'SlideShowName',
            'SlideShowImg',
            'Active',
        ]


# ------------------------ CART ------------------------
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = [
            'userId',
            'items',
            'productId',
            'name',
            'price',
            'qty',
            'img',
        ]


# ------------------------ RECEIPT ------------------------
class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = [
            'receiptId',
            'userId',
            'items',
            'quantity',
            'totalPayment',
            'paymentMethod',
            'date',
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'orderId',
            'user',
            'totalPayment',
            'paymentMethod',
            'date',
            'status',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryID', 'CategoryName']