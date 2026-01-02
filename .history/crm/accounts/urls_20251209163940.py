from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, LoginView, UserViewSet, ProductViewSet,
    SlideShowViewSet, CartViewSet, ReceiptViewSet, OrderViewSet,
    CategoryViewSet, LocationViewSet, save_location  # <-- IMPORT HERE
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'slideshows', SlideShowViewSet)
router.register(r'carts', CartViewSet)
router.register(r'receipts', ReceiptViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'location', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('location/save/', save_location),   # NOW Django knows the function
]
