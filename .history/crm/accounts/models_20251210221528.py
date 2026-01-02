from django.db import models
from django.conf import settings
from decimal import Decimal


# ------------------------------------------------------
# USER MODEL (Use Django default User, DO NOT override)
# ------------------------------------------------------
# settings.AUTH_USER_MODEL will point to Django's user model


# ------------------------------------------------------
# BANNERS
# ------------------------------------------------------
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"


# ------------------------------------------------------
# CATEGORY
# ------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# ------------------------------------------------------
# PRODUCTS
# ------------------------------------------------------
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        null=True, blank=True
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    description = models.TextField()
    rating = models.FloatField(default=0)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ------------------------------------------------------
# CART
# ------------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} cart: {self.product.name} x{self.quantity}"


# ------------------------------------------------------
# LOCATION
# ------------------------------------------------------
class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


# ------------------------------------------------------
# RECEIPT (Order Summary)
# ------------------------------------------------------
class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.id} - User {self.user}"


# ------------------------------------------------------
# RECEIPT ITEMS
# ------------------------------------------------------
class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


# ------------------------------------------------------
# TABLE BOOKING SYSTEM
# ------------------------------------------------------
class Table(models.Model):
    SEAT_CHOICES = [(i, f"{i} seats") for i in range(2, 7)]

    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(choices=SEAT_CHOICES)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("table", "date", "time")

    def __str__(self):
        return f"Reservation #{self.id} - Table {self.table.number}"
