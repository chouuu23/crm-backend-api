from django.db import models

# Create your models here.
# app_name/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password, not plain text

    def __str__(self):
        return self.name


class SlideShow(models.Model):
    ID = models.AutoField(primary_key=True)
    SlideShowName = models.CharField(max_length=255)
    SlideShowImg = models.ImageField(upload_to='slideshows/')
    Active = models.BooleanField(default=True)

    def __str__(self):
        return self.SlideShowName


class TblProducts(models.Model):
    productId = models.AutoField(primary_key=True)
    categoryId = models.IntegerField()  # You can change to ForeignKey if you have a Category table
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    rating = models.FloatField(default=0)
    isPopular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

