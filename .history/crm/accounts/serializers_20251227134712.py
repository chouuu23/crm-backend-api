from rest_framework import serializers
from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import (
    Products,
    Banner,
    Carts,
    Receipt,
    Order,
    Category,
    Location,
    Table,
    Reservation,
    Payment,
    TableBooking,
)

# ======================================================
# BANNER
# ======================================================

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ["id", "title", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return ""


# ======================================================
# REGISTER (JWT COMPATIBLE)
# ======================================================

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# ======================================================
# SESSION CART (FLUTTER WEB)
# ======================================================

class SessionCartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)
    img = serializers.CharField()


# ======================================================
# PRODUCT
# ======================================================

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


# ======================================================
# CART
# ======================================================

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = [
            "userId",
            "items",
            "productId",
            "name",
            "price",
            "qty",
            "img",
        ]


# ======================================================
# RECEIPT
# ======================================================

class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"

    def create(self, validated_data):
        items = validated_data.get("items", [])
        subtotal = sum(
            Decimal(item["price"]) * item.get("qty", 1)
            for item in items
        )

        delivery_fee = validated_data.get("delivery_fee", Decimal("1.50"))
        discount = validated_data.get("discount_amount", Decimal("0.00"))

        validated_data["subtotal"] = subtotal
        validated_data["total_amount"] = subtotal + delivery_fee - discount

        last_receipt = Receipt.objects.order_by("-id").first()
        next_id = (last_receipt.id + 1) if last_receipt else 1
        validated_data["receipt_number"] = f"R-{datetime.now().year}-{next_id:04d}"

        return super().create(validated_data)


# ======================================================
# ORDER
# ======================================================

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "orderId",
            "user",
            "totalPayment",
            "paymentMethod",
            "date",
            "status",
        ]


# ======================================================
# CATEGORY
# ======================================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["CategoryID", "CategoryName"]


# ======================================================
# LOCATION
# ======================================================

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


# ======================================================
# TABLE BOOKING (USER AUTO-ASSIGNED)
# ======================================================

class TableBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableBooking
        fields = "__all__"
        read_only_fields = [
            "user",
            "payment_status",
            "created_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)


# ======================================================
# TABLE
# ======================================================

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "seats", "is_reserved"]


# ======================================================
# RESERVATION
# ======================================================

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


# ======================================================
# PAYMENT (JWT PROTECTED)
# ======================================================

class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(
        source="booking.id",
        read_only=True
    )
    booking_customer = serializers.CharField(
        source="booking.customer_name",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "booking",
            "booking_id",
            "booking_customer",
            "amount",
            "method",
            "status",
            "transaction_id",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "transaction_id",
            "created_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
