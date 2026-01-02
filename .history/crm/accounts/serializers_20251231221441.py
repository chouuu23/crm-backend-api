from rest_framework import serializers
from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from .models import Favorite
from .models import Table, Reservation
from .models import (
    Products,
    Banner,
    Cart,
    Receipt,
    Order,
    Category,
    Location,
    Table,
    Reservation,
    Payment,
    TableBooking,
    Favorite,
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
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""


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

class CartProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="productId", read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ["id", "name", "price", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

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
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""


# ======================================================
# CART  ✅ FIXED & SAFE
# ======================================================
class CartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Cart
        fields = ["id", "product", "product_id", "quantity"]

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")

        product_id = validated_data.pop("product_id")
        quantity = validated_data.get("quantity", 1)

        try:
            product = Products.objects.get(productId=product_id)
        except Products.DoesNotExist:
            raise serializers.ValidationError({
                "product_id": "Invalid product ID"
            })

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart.quantity += quantity
            cart.save()

        return cart

    # ================== 🔥 THIS WAS MISSING 🔥 ==================
    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity")

        if quantity is None:
            raise serializers.ValidationError({
                "quantity": "This field is required."
            })

        if quantity <= 0:
            instance.delete()
            return instance

        instance.quantity = quantity
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "product_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data.pop("product_id")

        favorite, created = Favorite.objects.get_or_create(
            user=user,
            product_id=product_id
        )
        return favorite

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
        validated_data["receipt_number"] = (
            f"R-{datetime.now().year}-{next_id:04d}"
        )

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
# TABLE BOOKING
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
        if request:
            validated_data["user"] = request.user
        return super().create(validated_data)


# ======================================================
# TABLE
# ======================================================

class TableSerializer(serializers.ModelSerializer):
    is_reserved = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ["id", "number", "seats", "is_reserved"]

    def get_is_reserved(self, obj):
        request = self.context.get("request")
        if not request:
            return False

        date = request.query_params.get("date")
        time = request.query_params.get("time")

        if not date or not time:
            return False

        return Reservation.objects.filter(
            table=obj,
            date=date,
            time=time
        ).exists()

# ======================================================
# RESERVATION
# ======================================================

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "booking",
            "table",
            "guests",
            "date",
            "time",
        ]
        read_only_fields = ["id"]


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

    # ✅ RECEIPT (multipart-ready)
    receipt = serializers.ImageField(
        required=False,
        allow_null=True
    )

    receipt_url = serializers.SerializerMethodField()

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

            # ✅ receipt fields
            "receipt",
            "receipt_url",
            "receipt_uploaded_at",
            "approved_by_admin",
            "admin_note",

            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "transaction_id",
            "created_at",
            "receipt_uploaded_at",
            "approved_by_admin",
            "admin_note",
        ]

    def get_receipt_url(self, obj):
        request = self.context.get("request")
        if obj.receipt and request:
            return request.build_absolute_uri(obj.receipt.url)
        return None

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)