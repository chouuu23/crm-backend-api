from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("carts", CartViewSet)
router.register("tables", TableViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("cart/<int:user_id>/", user_cart),
    path("", include(router.urls)),
]
