from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
    ProductViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
    CategoryViewSet,
    LocationViewSet,
    TableViewSet,
    ReservationViewSet,
    BannerListAPIView,
    save_location,
    tables_api,
)

router = DefaultRouter()

# -----------------------
# API ROUTES
# -----------------------
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'receipts', ReceiptViewSet, basename='receipts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'reservations', ReservationViewSet, basename='reservations')

# -----------------------
# URL PATTERNS
# -----------------------
urlpatterns = [
    # ---------- AUTH ----------
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # ---------- CUSTOM ----------
    path('location/save/', save_location, name='save-location'),
    path('tables/available/', tables_api, name='tables-available'),
    path('banners/', BannerListAPIView.as_view(), name='banner-list'),

    # ---------- ROUTER ----------
    path('', include(router.urls)),
]
