from django.contrib import admin
from .models import (
    Banner,
    User,
    Category,
    Products,
    Carts,
    Receipt,
    Order,
    Location,
    TableBooking,
    Table,
)

# =========================
# TABLE ADMIN
# =========================
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")
    list_filter = ("seats",)
    ordering = ("number",)


# =========================
# SIMPLE REGISTRATIONS
# =========================
admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(Receipt)
admin.site.register(TableBooking)

# Order might already be registered
try:
    admin.site.register(Order)
except admin.sites.AlreadyRegistered:
    pass
