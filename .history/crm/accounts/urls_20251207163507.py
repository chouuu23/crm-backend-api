from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet,
    SlideShowViewSet, CartViewSet,
    ReceiptViewSet, CategoryViewSet,
    RegisterView
)

router = DefaultRouter()
router.register(r'Users', UserViewSet, basename='users')
router.register(r'Products', ProductViewSet, basename='products')
router.register(r'Slides', SlideShowViewSet, basename='slides')
router.register(r'Carts', CartViewSet, basename='carts')
router.register(r'Receipts', ReceiptViewSet, basename='receipts')
router.register(r'Categories', CategoryViewSet, basename='categories')  # only once!

urlpatterns = [
    path('', include(router.urls)),

    # Register API (NOT a viewset)
    path('register/', RegisterView.as_view(), name='register'),
]
