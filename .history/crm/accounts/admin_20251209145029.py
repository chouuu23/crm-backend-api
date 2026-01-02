from django.contrib import admin
from .models import Banner, User, Category, Products, SlideShow, Carts, Receipt, Order

# Register your models here.

admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Receipt)
admin.site.register(Order)
