from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    UserViewSet,
    ProductViewSet,
    SlideShowViewSet,
    CartViewSet,
    ReceiptViewSet,
)

router = DefaultRouter()
router.register(r'Users', UserViewSet, basename='user')
router.register(r'Products', ProductViewSet, basename='product')
router.register(r'SlideShow', SlideShowViewSet, basename='slideshow')
router.register(r'Carts', CartViewSet, basename='cart')
router.register(r'Receipts', ReceiptViewSet, basename='receipt')

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
    path('api/', include(router.urls)),
]

