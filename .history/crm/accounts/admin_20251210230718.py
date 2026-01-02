from django.contrib import admin
from .models import Banner, User, Category, Products, SlideShow, Carts, MyReceipt, Order,Location,TableBooking,Table



from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats', 'is_reserved')
    list_filter = ('seats', 'is_reserved')
    search_fields = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'user', 'guests', 'date', 'time', 'created_at')
    list_filter = ('date',)
    search_fields = ('table__number', 'user__username')


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

