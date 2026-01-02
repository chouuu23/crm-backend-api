from django.contrib import admin
from .models import (
    Banner, Category, Products, SlideShow, Carts,
    Location, Receipt, ReceiptItem, Order
)

# ---------------------------------------------------------
# SIMPLE MODELS
# ---------------------------------------------------------
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Location)


# ---------------------------------------------------------
# RECEIPT ITEM INLINE (For Admin UI)
# ---------------------------------------------------------
class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 0     # no empty rows
    readonly_fields = ("item_name", "price", "quantity", "total")


# ---------------------------------------------------------
# RECEIPT ADMIN
# ---------------------------------------------------------
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number", "user", "ordered_from",
        "delivered_to", "total_amount", "payment_method",
        "is_paid", "created_at"
    )

    list_filter = ("payment_method", "is_paid", "created_at")
    search_fields = ("receipt_number", "user__username", "ordered_from", "delivered_to")

    inlines = [ReceiptItemInline]


# ---------------------------------------------------------
# ORDER ADMIN
# ---------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("orderId", "user", "totalPayment", "paymentMethod", "status", "date")
    list_filter = ("status", "paymentMethod", "date")
    search_fields = ("orderId", "user__username")
