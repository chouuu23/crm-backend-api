from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    RegisterView,
    ProductViewSet,
    SlideShowViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'slideshows', SlideShowViewSet)
router.register(r'carts', CartViewSet)
router.register(r'receipts', ReceiptViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'Register', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserViewSet.as_view(), name='User'),
    path('products/', ProductViewSet.as_view(), name='Product'),
    path('slideshows/', SlideShowViewSet.as_view(), name='slideshows'),
    path('carts/', CartViewSet.as_view(), name='carts'),
    path('categories/', CategoryViewSet.as_view(), name='categories'),


]
