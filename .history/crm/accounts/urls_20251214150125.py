from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerListAPIView
from .views import tables_api

from .views import (
    RegisterView, LoginView, UserViewSet, ProductViewSet,
    CartViewSet, ReceiptViewSet, OrderViewSet,
    CategoryViewSet, LocationViewSet, save_location,TableBookingViewSet,TableViewSet,ReservationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet)
router.register(r'bookings', TableBookingViewSet)
router.register(r"receipts", ReceiptViewSet, basename="receipts")
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r"tables", TableViewSet, basename="tables")
router.register(r"reservations", ReservationViewSet, basename="reservations")


urlpatterns = [
    # custom path (must be above router)
    path('location/save/', save_location, name='save-location'),

    

    # router endpoints
    path('', include(router.urls)),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("tables/", tables_api),
    path('banners/', BannerListAPIView.as_view(), name='banner-list'),
]
