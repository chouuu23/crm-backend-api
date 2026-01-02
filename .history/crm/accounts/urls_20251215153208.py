from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("banners", BannerViewSet)
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("carts", CartViewSet)
router.register("orders", OrderViewSet)
router.register("locations", LocationViewSet)
router.register("receipts", ReceiptViewSet)
router.register("tables", TableViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("", include(router.urls)),
]
