from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, LoginView, UserViewSet, ProductViewSet,
    SlideShowViewSet, CartViewSet, MyReceiptViewSet, OrderViewSet,
    CategoryViewSet, LocationViewSet, save_location,TableBookingViewSet,TableViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'slideshows', SlideShowViewSet)
router.register(r'carts', CartViewSet)
router.register(r'bookings', TableBookingViewSet)
router.register(r'myreceipts', MyReceiptViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r"tables", TableViewSet)


urlpatterns = [
    # custom path (must be above router)
    path('location/save/', save_location, name='save-location'),

    # router endpoints
    path('', include(router.urls)),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
