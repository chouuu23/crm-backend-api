


from django.contrib import admin
from .models import (
    Banner,  Category, Products, SlideShow,
    Cart, Receipt, Order, Location,
    TableBooking, Table, Reservation
)



from django.contrib import admin
from .models import Payment

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = (
#         "booking",
#         "amount",
#         "method",
#         "status",
#         "created_at",
#     )
#     list_filter = ("method", "status", "created_at")
#     search_fields = ("booking__customer_name",)



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "booking",
        "amount",
        "method",
        "status",
        "approved_by_admin",
        "receipt_preview",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "status",
        "method",
        "approved_by_admin",
    )

    search_fields = (
        "booking__customer_name",
        "transaction_id",
    )

    ordering = ("method", "-created_at")

    readonly_fields = (
        "receipt_preview",
        "created_at",
        "receipt_uploaded_at",
    )

    fieldsets = (
        ("Payment Info", {
            "fields": (
                "booking",
                "user",
                "amount",
                "method",
                "status",
                "transaction_id",
            )
        }),
        ("Receipt", {
            "fields": (
                "receipt",
                "receipt_preview",
                "receipt_uploaded_at",
            )
        }),
        ("Admin Review", {
            "fields": (
                "approved_by_admin",
                "admin_note",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:120px;border-radius:6px;" />'
                '</a>',
                obj.receipt.url,
                obj.receipt.url,
            )
        return "No receipt"

    receipt_preview.short_description = "Receipt Preview"


# =======================
# CATEGORY ADMIN
# =======================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("categoryId", "categoryName")
    search_fields = ("categoryName",)


# =======================
# RESERVATION ADMIN
# =======================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "table",
        "guests",
        "date",
        "time",
        "created_at",
    )
    list_filter = ("date", "time")
    search_fields = ("user__username",)


from django.contrib import admin
from .models import TableBooking

@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'time',
        'guests',
        'customer_name',
        'customer_phone',
        'payment_method',
        'payment_status',
        'created_at',
    )

    list_filter = (
        'payment_method',
        'payment_status',
        'date',
    )

    search_fields = (
        'customer_name',
        'customer_phone',
    )



# =======================
# SIMPLE REGISTRATIONS
# =======================
admin.site.register(Banner)

admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Cart)
admin.site.register(Location)
admin.site.register(Receipt)

admin.site.register(Table)
admin.site.register(Order)
