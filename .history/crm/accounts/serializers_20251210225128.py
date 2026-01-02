from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Products,
    SlideShow,
    Carts,
    Receipt,
    ReceiptItem,
    Order,
    Category,
    Location,
    Table,
    Reservation,
    TableBooking,
)


# ------------------------ USER ------------------------
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


# ------------------------ LOGIN ------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        return {"id": user.id, "username": user.username, "email": user.email}


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

# ------------------------ PRODUCT ------------------------
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return ""


# ------------------------ SLIDE SHOW ------------------------
class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = "__all__"


# ------------------------ CART ------------------------
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = "__all__"


# ------------------------ RECEIPT ITEMS ------------------------
class ReceiptItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptItem
        fields = ["id", "name", "price", "quantity", "total"]

    def get_total(self, obj):
        return float(obj.price * obj.quantity)


# ------------------------ RECEIPT ------------------------
class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)
    delivered_to = serializers.CharField(source="location.name", read_only=True)
    delivered_time = serializers.DateTimeField(source="delivered_at", read_only=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "user",
            "location",
            "delivered_to",
            "subtotal",
            "delivery_fee",
            "vat_percent",
            "total_amount",
            "payment_method",
            "delivered_time",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        receipt = Receipt.objects.create(**validated_data)

        for item in items_data:
            ReceiptItem.objects.create(receipt=receipt, **item)

        return receipt


# ------------------------ ORDERS ------------------------
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


# ------------------------ CATEGORY ------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# ------------------------ LOCATION ------------------------
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


# ------------------------ TABLE BOOKING ------------------------
class TableBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableBooking
        fields = "__all__"


# ------------------------ TABLE ------------------------
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


# ------------------------ RESERVATION ------------------------
class ReservationSerializer(serializers.ModelSerializer):
    table_detail = TableSerializer(source="table", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "table",
            "table_detail",
            "guests",
            "date",
            "time",
            "created_at",
        ]
        read_only_fields = ["created_at"]
