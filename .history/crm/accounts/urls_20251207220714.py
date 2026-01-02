from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
   
    ProductViewSet,
    SlideShowViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
    CategoryViewSet,
    
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'slideshows', SlideShowViewSet, basename='slideshow')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'receipts', ReceiptViewSet, basename='receipt')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'categories', CategoryViewSet, basename='category')  # FIXED

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterViewSet.as_view(), name='register'),
    
]

