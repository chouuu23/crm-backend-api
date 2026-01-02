from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # auth
    RegisterView,
    LoginView,

    # viewsets
    UserViewSet,
    ProductViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
    CategoryViewSet,
    LocationViewSet,
    TableBookingViewSet,
    TableViewSet,
    ReservationViewSet,

    # custom apis
    save_location,
    tables_api,
    BannerListAPIView,

    # session cart (IMPORTANT FOR FLUTTER WEB)
    session_cart_get,
    session_cart_add,
    session_cart_decrease,
    session_cart_clear,
)

# ======================================================
# ROUTER
# ======================================================

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet)
router.register(r'receipts', ReceiptViewSet, basename='receipts')
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'bookings', TableBookingViewSet, basename='bookings')

# ======================================================
# URL PATTERNS
# ======================================================

urlpatterns = [
    # ---------- AUTH ----------
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # ---------- BANNERS ----------
    path('banners/', BannerListAPIView.as_view(), name='banner-list'),

    # ---------- TABLE AVAILABILITY ----------
    path('tables/available/', tables_api, name='tables-available'),

    # ---------- LOCATION ----------
    path('location/save/', save_location, name='save-location'),

    # ---------- SESSION CART (FLUTTER WEB SAFE) ----------
    path('session-cart/', session_cart_get, name='session-cart-get'),
    path('session-cart/add/', session_cart_add, name='session-cart-add'),
    path('session-cart/decrease/', session_cart_decrease, name='session-cart-decrease'),
    path('session-cart/clear/', session_cart_clear, name='session-cart-clear'),

    # ---------- ROUTER ----------
    path('', include(router.urls)),
]
