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


class Receipt(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True)

    user = models.ForeignKey("User", on_delete=models.CASCADE)

    ordered_from = models.CharField(max_length=255)
    delivered_to = models.CharField(max_length=255)

    delivered_at = models.DateTimeField()

    items = models.JSONField()   # [{"name": "Spaghetti", "price": 3.0, "qty": 1}, ...]

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("Cash on Delivery", "Cash on Delivery"),
            ("Online Payment", "Online Payment"),
        ],
        default="Cash on Delivery"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number}"






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

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"



class Reservation(models.Model):
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()

    tables = models.ManyToManyField(
        Table,
        related_name="reservations"
    )

    created_at = models.DateTimeField(auto_now_add=True)


    

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

# Table

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number}"


    


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






    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="foods/", blank=True, null=True)

    def __str__(self):
        return self.name


        

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

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

