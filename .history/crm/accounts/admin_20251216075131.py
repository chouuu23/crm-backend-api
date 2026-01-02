from django.contrib import admin
from .models import (
    Banner, User, Category, Products, SlideShow,
    Carts, Receipt, Order, Location,
    TableBooking, Table, Reservation
)

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
    list_display = ("id", "get_tables", "guests", "date", "time", "created_at")
    list_filter = ("date", "time")
    search_fields = ("user__username",)
    filter_horizontal = ("tables",)

    def get_tables(self, obj):
        return ", ".join(str(t.number) for t in obj.tables.all())

    get_tables.short_description = "Tables"


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
admin.site.register(User)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(Receipt)

admin.site.register(Table)
admin.site.register(Order)
