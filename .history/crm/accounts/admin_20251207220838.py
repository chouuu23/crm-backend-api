from django.contrib import admin
from .models import*
# Register your models here.

admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Receipt)
admin.site.register(Order)