from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.contrib.auth.models import User

from .models import (
    Banner, Products, Category, Carts,
    Order, Location, Receipt, Table, Reservation
)

from .serializers import (
    BannerSerializer, ProductSerializer, CategorySerializer,
    CartSerializer, OrderSerializer, LocationSerializer,
    ReceiptSerializer, TableSerializer, ReservationSerializer,
    UserSerializer, LoginSerializer
)


# ---------------- AUTH ----------------
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registered"})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


# ---------------- API ----------------
class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("userId")
        return Carts.objects.filter(user_id=user_id)

    @action(detail=False, methods=["post"])
    def add(self, request):
        item, _ = Carts.objects.get_or_create(
            user_id=request.data["userId"],
            product_id=request.data["productId"],
            defaults={"qty": 1}
        )
        item.qty += 1
        item.save()
        return Response({"success": True})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
