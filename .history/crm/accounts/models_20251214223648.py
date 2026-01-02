from django.db import models
from decimal import Decimal

# =========================
# BANNER
# =========================
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"


# =========================
# CUSTOM USER (APP USER)
# =========================
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="foods/", null=True, blank=True)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    isPopular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# =========================
# TABLE
# =========================
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"


# =========================
# TABLE BOOKING (MAIN BOOKING)
# =========================
class TableBooking(models.Model):
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    tables = models.ManyToManyField(
        Table,
        related_name="bookings"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.date} {self.time} - {self.guests} guests"


# =========================
# BOOKING ITEM (FOOD ORDERED)
# =========================
class BookingItem(models.Model):
    booking = models.ForeignKey(
        TableBooking,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


# =========================
# CART
# =========================
class Carts(models.Model):
    userId = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart {self.id} (User {self.userId})"


# =========================
# ORDER
# =========================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# =========================
# LOCATION
# =========================
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
