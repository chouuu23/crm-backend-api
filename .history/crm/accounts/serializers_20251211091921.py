from rest_framework import serializers
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from .models import User,Products, SlideShow, Carts, Receipt, Order,Category,Location,Table,Reservation
# Imports Users, Products, TblSlideShow, TblCarts, TblReceipt


from .models import Receipt,TableBooking

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
    # Explicitly add the choice field (fixes "not a valid choice" bug)
    payment_method = serializers.ChoiceField(
        choices=[
            ("Cash on Delivery", "Cash on Delivery"),
            ("Online Payment", "Online Payment"),
        ]
    )

    class Meta:
        model = Receipt
        fields = "__all__"

    def validate_items(self, value):
        """
        Ensure items is always a list of dicts, not JSON string
        """
        if isinstance(value, str):
            try:
                import json
                value = json.loads(value)
            except:
                raise serializers.ValidationError("Invalid items format.")
        return value

    def create(self, validated_data):
        items = validated_data["items"]

        # Ensure items is a list
        if isinstance(items, str):
            import json
            items = json.loads(items)

        subtotal = sum(
            [Decimal(item["price"]) * item.get("qty", 1) for item in items]
        )

        delivery_fee = Decimal(validated_data.get("delivery_fee", 1.50))
        discount = Decimal(validated_data.get("discount_amount", 0))

        total = subtotal + delivery_fee - discount

        validated_data["subtotal"] = subtotal
        validated_data["total_amount"] = total

        # Auto-generate receipt number
        last_receipt = Receipt.objects.order_by("-id").first()
        next_id = (last_receipt.id + 1) if last_receipt else 1
        validated_data["receipt_number"] = f"R-{datetime.now().year}-{next_id:04d}"

        return super().create(validated_data)

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

class TableBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableBooking
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'seats', 'is_reserved']


class ReservationSerializer(serializers.ModelSerializer):
    # Provide nested table info read-only
    table_detail = TableSerializer(source="table", read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'table_detail', 'guests', 'date', 'time', 'created_at']
        read_only_fields = ['created_at']