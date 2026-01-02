
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet

router = DefaultRouter()
router.register('Users', UserViewSet, basename='user')
router.register('Products', ProductsViewSet, basename='product')

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
    path('api/', include(router.urls)),   # /api/students/
]

