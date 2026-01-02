from django.db import models
from django.contrib.auth.models import User


class Login(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

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
    receiptId = models.AutoField(primary_key=True)
    userId = models.IntegerField()
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
