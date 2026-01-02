from django.contrib import admin
from .models import (
    Banner,
    Category,
    Products,
    Carts,
    Location,
    Receipt,
    ReceiptItem,
    Table,
    Reservation,
    SlideShow,
)

admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(Receipt)
admin.site.register(ReceiptItem)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(SlideShow)
