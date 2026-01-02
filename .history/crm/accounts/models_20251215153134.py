from django.db import models
from django.conf import settings
from decimal import Decimal

# -------------------------
# BANNER
# -------------------------
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"


# -------------------------
# CATEGORY
# -------------------------
class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.categoryName


# -------------------------
# PRODUCT
# -------------------------
class Products(models.Model):
    productId = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    description = models.TextField()
    rating = models.FloatField(default=0)
    isPopular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# -------------------------
# CART
# -------------------------
class Carts(models.Model):
    cartId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "product")


# -------------------------
# ORDER
# -------------------------
class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------
# LOCATION
# -------------------------
class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------
# RECEIPT
# -------------------------
class Receipt(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    payment_method = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------
# TABLE
# -------------------------
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number}"


# -------------------------
# RESERVATION
# -------------------------
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tables = models.ManyToManyField(Table)
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
