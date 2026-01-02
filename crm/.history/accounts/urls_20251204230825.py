
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from accounts.views import StudentViewSet

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
    path('api/', include(router.urls)),   # /api/students/
]

