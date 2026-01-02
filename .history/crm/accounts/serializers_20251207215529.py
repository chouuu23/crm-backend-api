from rest_framework import serializers
from .models import Register,Products, SlideShow, Carts, Receipt, Order,Category
# Imports Users, Products, TblSlideShow, TblCarts, TblReceipt


# ------------------------ USER ------------------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['userId', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs



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