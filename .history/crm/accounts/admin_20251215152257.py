from django.contrib import admin
from django.contrib.auth.models import User

from .models import (
    Profile,
    Banner,
    Category,
    Products,
    Carts,
    Order,
    Location,
    Receipt,
    ReceiptItem,
    Table,
    Reservation,
)

# =======================
# USER PROFILE
# =======================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone")
    search_fields = ("user__username", "name", "phone")


# =======================
# CATEGORY
# =======================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("categoryId", "categoryName")
    search_fields = ("categoryName",)


# =======================
# PRODUCT
# =======================
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("productId", "name", "price", "isPopular")
    list_filter = ("isPopular", "category")
    search_fields = ("name",)


# =======================
# CART
# =======================
@admin.register(Carts)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cartId", "user", "product", "qty")
    search_fields = ("user__username", "product__name")


# =======================
# ORDER
# =======================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("orderId", "user", "totalPayment", "paymentMethod", "status", "created_at")
    list_filter = ("status", "paymentMethod")
    search_fields = ("user__username",)


# =======================
# LOCATION
# =======================
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone", "created_at")
    search_fields = ("user__username", "phone")


# =======================
# RECEIPT
# =======================
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "user", "total_amount", "payment_method", "is_paid", "created_at")
    list_filter = ("payment_method", "is_paid")
    search_fields = ("receipt_number", "user__username")


@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ("receipt", "item_name", "quantity", "price")


# =======================
# TABLE
# =======================
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")
    list_filter = ("seats",)


# =======================
# RESERVATION
# =======================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "get_tables", "guests", "date", "time", "created_at")
    list_filter = ("date", "time")
    search_fields = ("user__username",)
    filter_horizontal = ("tables",)

    def get_tables(self, obj):
        return ", ".join(str(t.number) for t in obj.tables.all())

    get_tables.short_description = "Tables"
