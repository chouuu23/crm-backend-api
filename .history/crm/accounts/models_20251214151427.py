from django.db import models
from decimal import Decimal

# =========================
# USER (CUSTOM – SIMPLE)
# =========================
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # plain text (current DB)

    def __str__(self):
        return self.name


# =========================
# BANNER
# =========================
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# CATEGORY
# =========================
class Category(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.CategoryName


# =========================
# PRODUCT
# =========================
class Products(models.Model):
    productId = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
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


# =========================
# CART
# =========================
class Carts(models.Model):
    cartId = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    productId = models.IntegerField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    img = models.ImageField(upload_to='cart_items/', null=True, blank=True)

    def __str__(self):
        return f"User {self.userId} - {self.name}"


# =========================
# ORDER
# =========================
class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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


# =========================
# RECEIPT (SINGLE VERSION)
# =========================
class Receipt(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ordered_from = models.CharField(max_length=255)
    delivered_to = models.CharField(max_length=255)
    delivered_at = models.DateTimeField()

    items = models.JSONField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# LOCATION
# =========================
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# TABLE
# =========================
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number}"


# =========================
# TABLE BOOKING
# =========================
class TableBooking(models.Model):
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
