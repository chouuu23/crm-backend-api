from django.contrib import admin
from .models import Banner, User, Category, Products, SlideShow, Carts, MyReceipt, Order,Location,TableBooking

admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(MyReceipt)
admin.site.register(TableBooking)
admin.site.register(Table)

# Avoid duplicate registration
try:
    admin.site.register(Order)
except admin.sites.AlreadyRegistered:
    pass

