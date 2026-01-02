from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, LoginView, UserViewSet, ProductViewSet,
    SlideShowViewSet, CartViewSet, MyReceiptSerializer, OrderViewSet,
    CategoryViewSet, LocationViewSet, save_location
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'slideshows', SlideShowViewSet)
router.register(r'carts', CartViewSet)
router.register(r'receipts', MyReceiptSerializer, basename="receipt")
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'location', LocationViewSet)

urlpatterns = [
    # custom path (must be above router)
    path('location/save/', save_location, name='save-location'),

    # router endpoints
    path('', include(router.urls)),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
