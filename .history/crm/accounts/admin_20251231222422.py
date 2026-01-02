from django.contrib import admin
from .models import Payment

from django.utils.html import format_html
from django.contrib import messages
from django.utils import timezone

from django.contrib import admin
from .models import (
    Banner,  Category, Products, SlideShow,
    Cart, Receipt, Order, Location,
    TableBooking, Table, Reservation
)





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

    list_filter = ("status", "method", "approved_by_admin")
    search_fields = ("booking__customer_name", "transaction_id")
    ordering = ("method", "-created_at")

    readonly_fields = (
        "receipt_preview",
        "created_at",
        "receipt_uploaded_at",
    )

    actions = ["approve_payments", "reject_payments"]

    # ================= ADMIN ACTIONS =================

    def approve_payments(self, request, queryset):
        count = 0
        for payment in queryset:
            if not payment.receipt:
                continue  # ❌ must have receipt

            if payment.status == "PAID":
                continue

            payment.status = "PAID"
            payment.approved_by_admin = True
            payment.admin_note = ""
            payment.save()

            booking = payment.booking
            booking.payment_status = "paid"
            booking.payment_method = payment.method
            booking.save()

            count += 1

        self.message_user(
            request,
            f"{count} payment(s) approved successfully.",
            messages.SUCCESS
        )

    approve_payments.short_description = "Approve selected payments"

    def reject_payments(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status == "PAID":
                continue  # ❌ cannot reject paid

            payment.status = "REJECTED"
            payment.approved_by_admin = False
            payment.admin_note = "Rejected by admin"
            payment.save()

            count += 1

        self.message_user(
            request,
            f"{count} payment(s) rejected.",
            messages.WARNING
        )

    reject_payments.short_description = "Reject selected payments"

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
