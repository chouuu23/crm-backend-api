from django.db import models
from decimal import Decimal

# =========================
# CATEGORY
# =========================
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


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
    image = models.ImageField(upload_to="foods/", blank=True, null=True)

    def __str__(self):
        return self.name


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

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    tables = models.ManyToManyField(
        Table,
        related_name="bookings"
    )

    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
