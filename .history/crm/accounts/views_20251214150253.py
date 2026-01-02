from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view

from .models import (
    User, Banner, Products, Carts, Receipt, Order,
    Category, Location, TableBooking, Table, Reservation
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, CartSerializer,
    ReceiptSerializer, OrderSerializer,
    CategorySerializer, LocationSerializer,
    TableBookingSerializer, TableSerializer,
    ReservationSerializer, BannerSerializer
)

from rest_framework.generics import ListAPIView
from .table_service import available_tables


# ======================================================
# BASIC TEST
# ======================================================
def home(request):
    return HttpResponse("Home_page")


# ======================================================
# REGISTER
# ======================================================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": 200, "message": "User registered", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)


# ======================================================
# LOGIN
# ======================================================
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"status": 200, "message": "Login successful", "data": serializer.validated_data},
                status=200
            )
        return Response({"errors": serializer.errors}, status=400)


# ======================================================
# VIEWSETS
# ======================================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-userId')
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Products.objects.all().order_by('-productId')
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all().order_by('-cartId')
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('CategoryName')
    serializer_class = CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('-id')
    serializer_class = LocationSerializer


class TableBookingViewSet(viewsets.ModelViewSet):
    queryset = TableBooking.objects.all()
    serializer_class = TableBookingSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('number')
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('-created_at')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ======================================================
# RECEIPT
# ======================================================
class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('-created_at')
    serializer_class = ReceiptSerializer


# ======================================================
# BANNER
# ======================================================
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


# ======================================================
# TABLE AVAILABILITY API
# ======================================================
@api_view(["GET"])
def tables_api(request):
    date = request.GET.get("date")
    time = request.GET.get("time")
    seats = int(request.GET.get("seats"))

    tables = available_tables(date, time, seats)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


# ======================================================
# LOCATION SAVE (SIMPLE)
# ======================================================
@api_view(['POST'])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location saved", "data": serializer.data})
    return Response(serializer.errors, status=400)


# ======================================================
# 🔥 CART PERSISTENCE (FLUTTER)
# ======================================================
@api_view(["GET"])
def get_user_cart(request):
    user_id = request.GET.get("userId")
    if not user_id:
        return Response({"error": "userId required"}, status=400)

    cart_items = Carts.objects.filter(userId=user_id)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def save_user_cart(request):
    user_id = request.data.get("userId")
    items = request.data.get("items", [])

    if not user_id:
        return Response({"error": "userId required"}, status=400)

    Carts.objects.filter(userId=user_id).delete()

    for item in items:
        Carts.objects.create(
            userId=user_id,
            productId=item["productId"],
            name=item["name"],
            price=item["price"],
            qty=item["quantity"],
        )

    return Response({"status": "cart saved"})
