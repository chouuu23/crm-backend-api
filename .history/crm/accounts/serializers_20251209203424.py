from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password
from .models import User,Products, SlideShow, Carts, Receipt, Order,Category,Location
# Imports Users, Products, TblSlideShow, TblCarts, TblReceipt



# app/serializers.py
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from rest_framework import serializers

from .models import Receipt, ReceiptItem


def quantize_two(value: Decimal) -> Decimal:
    """Helper to quantize Decimal values to 2 decimal places."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class ReceiptItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReceiptItem
        fields = ("id", "item_name", "price", "quantity", "total")
        read_only_fields = ("id", "total")

    def get_total(self, obj):
        return quantize_two(Decimal(obj.price) * Decimal(obj.quantity))


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Receipt
        fields = (
            "id",
            "receipt_number",
            "user",
            "ordered_from",
            "delivered_to",
            "created_at",
            "delivered_at",
            "items",
            "subtotal",
            "delivery_fee",
            "discount_amount",
            "total_amount",
            "payment_method",
            "is_paid",
        )
        read_only_fields = ("id", "created_at", "subtotal", "total_amount")

    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one item is required.")
        for it in value:
            # price and quantity basic checks
            price = Decimal(str(it.get("price", 0)))
            quantity = int(it.get("quantity", 1))
            if price <= 0:
                raise serializers.ValidationError("Each item price must be greater than 0.")
            if quantity <= 0:
                raise serializers.ValidationError("Each item quantity must be at least 1.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        # set user from context request if available AND not provided explicitly
        request = self.context.get("request")
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            validated_data["user"] = request.user

        # Create the receipt
        receipt = Receipt.objects.create(**validated_data)

        # Create items and compute subtotal
        subtotal = Decimal("0.00")
        for item in items_data:
            item_obj = ReceiptItem.objects.create(
                receipt=receipt,
                item_name=item["item_name"],
                price=Decimal(str(item["price"])),
                quantity=int(item.get("quantity", 1)),
            )
            subtotal += (item_obj.price * item_obj.quantity)

        # Compute totals server-side
        receipt.subtotal = quantize_two(subtotal)
        delivery_fee = Decimal(str(receipt.delivery_fee or "0.00"))
        discount = Decimal(str(receipt.discount_amount or "0.00"))
        total = subtotal + delivery_fee - discount
        receipt.total_amount = quantize_two(total if total >= 0 else Decimal("0.00"))
        receipt.save()
        return receipt

    @transaction.atomic
    def update(self, instance, validated_data):
        # Support updating receipt fields and replacing items if provided
        items_data = validated_data.pop("items", None)

        # Update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            # Replace items (simple approach)
            instance.items.all().delete()
            subtotal = Decimal("0.00")
            for item in items_data:
                item_obj = ReceiptItem.objects.create(
                    receipt=instance,
                    item_name=item["item_name"],
                    price=Decimal(str(item["price"])),
                    quantity=int(item.get("quantity", 1)),
                )
                subtotal += (item_obj.price * item_obj.quantity)

            instance.subtotal = quantize_two(subtotal)
            delivery_fee = Decimal(str(instance.delivery_fee or "0.00"))
            discount = Decimal(str(instance.discount_amount or "0.00"))
            total = subtotal + delivery_fee - discount
            instance.total_amount = quantize_two(total if total >= 0 else Decimal("0.00"))
            instance.save()
        else:
            # If items not provided, ensure totals reflect any possibly changed fees/discounts
            subtotal = instance.subtotal or Decimal("0.00")
            delivery_fee = Decimal(str(instance.delivery_fee or "0.00"))
            discount = Decimal(str(instance.discount_amount or "0.00"))
            total = subtotal + delivery_fee - discount
            instance.total_amount = quantize_two(total if total >= 0 else Decimal("0.00"))
            instance.save()

        return instance



# ------------------------ USER ------------------------
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    
# ------------------------ REGISTER ------------------------

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'password', 'confirm_password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"errors": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        # Store raw password (NOT hashed)
        return User.objects.create(**validated_data)

    
# ------------------------ LOG IN ------------------------

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": "Email not found"})

        # Compare directly since password is NOT hashed
        if password != user.password:
            raise serializers.ValidationError({"errors": "Incorrect password"})

        return {
            "userId": user.userId,
            "name": user.name,
            "email": user.email,
        }


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

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'