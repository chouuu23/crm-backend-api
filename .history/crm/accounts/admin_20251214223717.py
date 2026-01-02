from django.contrib import admin
from .models import (
    Banner, User, Category, Product,
    Table, TableBooking, BookingItem,
    Carts, Order, Location
)

# =========================
# INLINE FOOD ITEMS
# =========================
class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 1


# =========================
# TABLE BOOKING ADMIN
# =========================
@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "guests", "customer_name")
    inlines = [BookingItemInline]


# =========================
# TABLE ADMIN
# =========================
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")
    ordering = ("number",)


# =========================
# SIMPLE REGISTRATIONS
# =========================
admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Carts)
admin.site.register(Order)
admin.site.register(Location)
