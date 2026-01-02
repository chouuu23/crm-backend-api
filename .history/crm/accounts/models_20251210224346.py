from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal



class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')  # upload to /media/banners/
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Banner {self.id}"

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# -----------------------------
# FIXED CATEGORY MODEL
# -----------------------------
class Category(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.CategoryName

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


class Carts(models.Model):
    cartId = models.AutoField(primary_key=True)
    userId = models.IntegerField()     
    productId = models.IntegerField()  
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    img = models.ImageField(upload_to='cart_items/', null=True, blank=True)
    items = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Cart for User {self.userId} - {self.name}"


class MyReceipt(models.Model):
    receiptId = models.AutoField(primary_key=True)
    userId = models.IntegerField()

    # NEW FIELD
    location = models.CharField(max_length=255, null=True, blank=True)

    items = models.TextField()
    quantity = models.IntegerField()
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receiptId} - User {self.userId}"



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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50, default="cash")
    delivered_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.id}"


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} x {self.quantity}"

class TableBooking(models.Model):
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()

    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.date} {self.time} - {self.guests} guests"
    

class Table(models.Model):
    SEAT_CHOICES = [(i, f"{i} Seats") for i in range(2, 7)]

    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(choices=SEAT_CHOICES)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats) - {'Reserved' if self.is_reserved else 'Available'}"


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="reservations")
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("table", "date", "time")  # prevents double-booking the same table at same slot

    def __str__(self):
        return f"Reservation #{self.id} - {self.table} for {self.guests} on {self.date} {self.time}"