from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, LoginView, UserViewSet, ProductViewSet,
    CartViewSet, ReceiptViewSet, OrderViewSet,
    CategoryViewSet, LocationViewSet, save_location,
    TableBookingViewSet, TableViewSet,
    get_user_cart, save_user_cart
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet)
router.register(r'bookings', TableBookingViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'locations', LocationViewSet)
router.register(r"tables", TableViewSet, basename="tables")

urlpatterns = [
    # CART PERSISTENCE (FLUTTER)
    path("cart/user/", get_user_cart),
    path("cart/save/", save_user_cart),

    # location
    path('location/save/', save_location),

    # router endpoints
    path('', include(router.urls)),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
