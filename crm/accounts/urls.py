from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .auth_views import JWTLoginView, RegisterView, MeView
from .views import (
    ProductViewSet,
    CartViewSet,
    ReceiptViewSet,
    OrderViewSet,
    CategoryViewSet,
    LocationViewSet,
    TableBookingViewSet,
    TableViewSet,
    ReservationViewSet,
    PaymentViewSet,
    cart_decrease,
    save_location,
    tables_api,
    BannerListAPIView,
    FavoriteViewSet,
    AdminDashboardStatsAPIView,
    AdminRecentBookingsAPIView,
    AdminRecentPaymentsAPIView,
    AdminUserListAPIView,
    AdminPaymentListAPIView,
    AdminBookingListAPIView,
    AdminProfileAPIView,
    BestSellingProductsAPIView,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'receipts', ReceiptViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'bookings', TableBookingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),

    # AUTH
    path("login/", JWTLoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("me/", MeView.as_view()),

    # OTHER
    path('banners/', BannerListAPIView.as_view()),
    path('tables/available/', tables_api),
    path("carts/decrease/", cart_decrease),
    path('location/save/', save_location),
    path("admin/dashboard/stats/", AdminDashboardStatsAPIView.as_view()),
    path("admin/dashboard/recent-bookings/", AdminRecentBookingsAPIView.as_view()),
    path("admin/dashboard/recent-payments/", AdminRecentPaymentsAPIView.as_view()),
    path("admin/users/", AdminUserListAPIView.as_view()),
    path("admin/payments/", AdminPaymentListAPIView.as_view()),
    path("admin/bookings/", AdminBookingListAPIView.as_view()),
    path("admin/profile/", AdminProfileAPIView.as_view()),
    path("admin/dashboard/best-selling-products/",BestSellingProductsAPIView.as_view()),
]
