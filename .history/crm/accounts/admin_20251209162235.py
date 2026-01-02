from django.contrib import admin
from .models import (
    Banner, User, Category, Products, SlideShow,
    Carts, Receipt, Order, Location
)

# Register models (no duplicates)
models_to_register = [
    Banner, User, Category, Products, SlideShow,
    Carts, Receipt, Order, Location
]

for model in models_to_register:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
