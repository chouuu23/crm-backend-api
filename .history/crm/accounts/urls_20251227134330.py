from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .auth_views import JWTLoginView

from .views import (
    # AUTH
    RegisterView,
    LoginView,

    # VIEWSETS
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
    PaymentViewSet,

    # OTHER APIs
    save_location,
    tables_api,
    BannerListAPIView,

    # SESSION CART
    session_cart_get,
    session_cart_add,
    session_cart_decrease,
    session_cart_clear,
)

# ======================================================
# ROUTER
# ======================================================

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'receipts', ReceiptViewSet, basename='receipts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'bookings', TableBookingViewSet, basename='bookings')
router.register(r'payments', PaymentViewSet, basename='payments')

# ======================================================
# URL PATTERNS
# ======================================================

urlpatterns = [
    # ROUTER
    path('', include(router.urls)),

    # AUTH
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # BANNERS
    path('banners/', BannerListAPIView.as_view(), name='banner-list'),

    # TABLE AVAILABILITY
    path('tables/available/', tables_api, name='tables-available'),

    # LOCATION
    path('location/save/', save_location, name='save-location'),

    # SESSION CART
    path('session-cart/', session_cart_get, name='session-cart-get'),
    path('session-cart/add/', session_cart_add, name='session-cart-add'),
    path('session-cart/decrease/', session_cart_decrease, name='session-cart-decrease'),
    path('session-cart/clear/', session_cart_clear, name='session-cart-clear'),
]
