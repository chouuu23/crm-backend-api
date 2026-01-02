from django.contrib import admin
from .models import (
    Banner, User, Category, Products, SlideShow,
    Carts, Receipt, Order, Location,
    TableBooking, Table, Reservation, BookingItem
)

# =======================
# INLINE FOOD ITEMS
# =======================
class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 1

# =======================
# TABLE BOOKING ADMIN
# =======================
@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "guests", "customer_name")
    inlines = [BookingItemInline]

# =======================
# TABLE ADMIN
# =======================
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")
    list_filter = ("seats",)
    ordering = ("number",)

# =======================
# RESERVATION ADMIN
# =======================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_tables", "guests", "date", "time", "created_at")
    list_filter = ("date", "time")
    search_fields = ("user__username",)
    filter_horizontal = ("tables",)

    def get_tables(self, obj):
        return ", ".join(str(t.number) for t in obj.tables.all())

    get_tables.short_description = "Tables"

# =======================
# SIMPLE REGISTRATIONS
# =======================
admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(Receipt)

# Avoid duplicate registration for Order
try:
    admin.site.register(Order)
except admin.sites.AlreadyRegistered:
    pass
