from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    UserViewSet,
    ProductViewSet,
    SlideShowViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register(r'Users', UserViewSet, basename='user')
router.register(r'Products', ProductViewSet, basename='product')
router.register(r'SlideShow', SlideShowViewSet, basename='slideshow')
router.register(r'Carts', CartViewSet, basename='cart')
router.register(r'Receipts', ReceiptViewSet, basename='receipt')
router.register(r'Orders', OrderViewSet, basename='order')

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
    path('api/', include(router.urls)),
    path('SlideShow/', views.SlideShow),
    path('Orders/', views.Order),
    path('Carts/', views.Carts),
]

# ADD THIS:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

