from django.db import models

# Create your models here.
# app_name/models.py
from django.db import models

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords

    def __str__(self):
        return self.name
    
class Category(models.Model):
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
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
        related_name='products'
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
    userId = models.IntegerField()                    # Replace with ForeignKey if TblUsers exists
    productId = models.IntegerField()                 # Replace with FK to TblProducts if needed
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    img = models.ImageField(upload_to='cart_items/', null=True, blank=True)
    items = models.TextField(null=True, blank=True)   # Optional: JSON string of cart details

    def __str__(self):
        return f"Cart for User {self.userId} - {self.name}"


class Receipt(models.Model):
    receiptId = models.AutoField(primary_key=True)
    userId = models.IntegerField()                    # Replace with FK to TblUsers if needed
    items = models.TextField()                        # Store JSON or text list of purchased items
    quantity = models.IntegerField()
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receiptId} - User {self.userId}"

from django.db import models
from django.contrib.auth.models import User  # if you use Django User model

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
    


