from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("ABA", "ABA Pay"),
        ("CASH", "Cash on Delivery"),
        ("CARD", "Credit / Debit Card"),
    ]

    PAYMENT_STATUS = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REJECTED", "Rejected"),  # ✅ for admin rejection
    ]

    booking = models.OneToOneField(
        "accounts.TableBooking",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="PENDING"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ================= RECEIPT =================
    receipt = models.ImageField(
        upload_to="payment_receipts/",
        null=True,
        blank=True
    )

    receipt_uploaded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ================= ADMIN CONTROL =================
    approved_by_admin = models.BooleanField(default=False)
    admin_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.customer_name} - {self.amount} ({self.status})"


class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')  # upload to /media/banners/
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Banner {self.id}"


# -----------------------------
# FIXED CATEGORY MODEL
# -----------------------------
class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["categoryName"]

    def __str__(self):
        return self.categoryName

class SlideShow(models.Model):
    ID = models.AutoField(primary_key=True)
    SlideShowName = models.CharField(max_length=255)
    SlideShowImg = models.ImageField(upload_to='slideshows/')
    Active = models.BooleanField(default=True)

    def __str__(self):
        return self.SlideShowName


class Products(models.Model):
    productId = models.AutoField(primary_key=True)
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    related_name='products',
    null=True,     # allow existing rows to be null
    blank=True
)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    rating = models.FloatField(default=0)
    isPopular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


User = get_user_model()



class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"






class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


    
class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.orderId} - User {self.user.id}"

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Receipt(models.Model):
    PAYMENT_METHODS = (
        ("cod", "Cash on Delivery"),
        ("card", "Credit Card"),
        ("wallet", "Wallet"),
    )

    # Example: rhak-2534-w6s0
    receipt_number = models.CharField(max_length=50, unique=True)

    # User who made the order
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receipts")

    # Delivery information
    ordered_from = models.CharField(max_length=255)
    delivered_to = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Price breakdown
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cod")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Receipt #{self.receipt_number}"
    
class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"




class TableBooking(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('none', 'Not Selected'),
        ('shop', 'Pay at Shop'),
        ('aba', 'ABA Pay'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="table_bookings"
    )

    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()

    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='none'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.date} {self.time} - {self.guests} guests"

    



class Table(models.Model):
    SEAT_CHOICES = [(i, f"{i} Seats") for i in range(2, 7)]

    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(choices=SEAT_CHOICES)
    
    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(TableBooking, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations")
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ ADD THIS

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["table", "date", "time"],
                name="unique_table_time_slot"
            )
        ]
class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    guests = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

    table = models.IntegerField()
    seats = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

class FoodOrder(models.Model):
    booking = models.ForeignKey(Booking, related_name="foods", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    quantity = models.IntegerField()
    img = models.URLField()