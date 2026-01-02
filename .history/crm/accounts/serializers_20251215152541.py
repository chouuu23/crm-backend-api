from rest_framework import serializers
from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from .models import (
    Profile,
    Banner,
    Products,
    Category,
    Carts,
    Order,
    Location,
    Receipt,
    ReceiptItem,
    Table,
    Reservation,
)

# --------------------------------------------------
# BANNER
# --------------------------------------------------
class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ["id", "title", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ""


# --------------------------------------------------
# USER (DJANGO AUTH)
# --------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }


# --------------------------------------------------
# CATEGORY
# --------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["categoryId", "categoryName"]


# --------------------------------------------------
# PRODUCT
# --------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ""


# --------------------------------------------------
# CART
# --------------------------------------------------
class CartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Carts
        fields = ["cartId", "name", "price", "qty"]


# --------------------------------------------------
# ORDER
# --------------------------------------------------
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "orderId",
            "user",
            "totalPayment",
            "paymentMethod",
            "status",
            "created_at",
        ]
        read_only_fields = ["created_at"]


# --------------------------------------------------
# LOCATION
# --------------------------------------------------
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


# --------------------------------------------------
# RECEIPT
# --------------------------------------------------
class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = ["item_name", "price", "quantity"]


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = "__all__"
        read_only_fields = ["receipt_number", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        subtotal = sum(
            Decimal(item["price"]) * item["quantity"] for item in items_data
        )

        delivery_fee = validated_data.get("delivery_fee", Decimal("0.00"))
        discount = validated_data.get("discount_amount", Decimal("0.00"))
        total = subtotal + delivery_fee - discount

        validated_data["subtotal"] = subtotal
        validated_data["total_amount"] = total

        last_receipt = Receipt.objects.order_by("-id").first()
        next_id = last_receipt.id + 1 if last_receipt else 1
        validated_data["receipt_number"] = f"R-{datetime.now().year}-{next_id:04d}"

        receipt = Receipt.objects.create(**validated_data)

        for item in items_data:
            ReceiptItem.objects.create(
                receipt=receipt,
                item_name=item["item_name"],
                price=item["price"],
                quantity=item["quantity"],
            )

        return receipt


# --------------------------------------------------
# TABLE
# --------------------------------------------------
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "seats"]


# --------------------------------------------------
# RESERVATION (TABLE BOOKING)
# --------------------------------------------------
class ReservationSerializer(serializers.ModelSerializer):
    tables_detail = TableSerializer(source="tables", many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "tables",
            "tables_detail",
            "guests",
            "date",
            "time",
            "created_at",
        ]
        read_only_fields = ["created_at"]
