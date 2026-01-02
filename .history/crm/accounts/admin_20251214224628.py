from django.contrib import admin
from .models import  Category, TableBooking,Table
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")
    list_filter = ("seats",)
    ordering = ("number",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_tables", "guests", "date", "time", "created_at")
    list_filter = ("date", "time")
    search_fields = ("user__username",)
    filter_horizontal = ("tables",)

    def get_tables(self, obj):
        return ", ".join(str(t.number) for t in obj.tables.all())

    get_tables.short_description = "Tables"


admin.site.register(Banner)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(SlideShow)
admin.site.register(Carts)
admin.site.register(Location)
admin.site.register(Receipt)
admin.site.register(TableBooking)


# Avoid duplicate registration
try:
    admin.site.register(Order)
except admin.sites.AlreadyRegistered:
    pass

