from rest_framework import serializers
from .models import Users, Products, SlideShow, Carts, Receipt
# Imports Users, Products, TblSlideShow, TblCarts, TblReceipt


# ------------------------ USER ------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userId', 'name', 'email', 'password']


# ------------------------ PRODUCT ------------------------
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
        model = TblReceipt
        fields = [
            'receiptId',
            'userId',
            'items',
            'quantity',
            'totalPayment',
            'paymentMethod',
            'date',
        ]
