from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from .models import (
    User,
    Banner,
    Products,
    Carts,
    Receipt,
    Order,
    Category,
    Location,
    Table,
    TableBooking,
    Reservation,
)

from .serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    ProductSerializer,
    CartSerializer,
    ReceiptSerializer,
    OrderSerializer,
    CategorySerializer,
    LocationSerializer,
    TableSerializer,
    TableBookingSerializer,
    ReservationSerializer,
)

from .table_service import available_tables


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
# BANNERS
# ======================================================
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


# ======================================================
# REGISTER
# ======================================================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": "User registered successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
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
                {
                    "status": 200,
                    "message": "Login successful",
                    "data": serializer.validated_data,
                }
            )
        return Response({"errors": serializer.errors}, status=400)


# ======================================================
# USER
# ======================================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-userId")
    serializer_class = UserSerializer


# ======================================================
# PRODUCT
# ======================================================
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Products.objects.all().order_by("-productId")
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


# ======================================================
# CART
# ======================================================
class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all().order_by("-cartId")
    serializer_class = CartSerializer


# ======================================================
# LOAD CART BY USER (IMPORTANT FOR RESTORE)
# ======================================================
@api_view(["GET"])
def user_cart(request, user_id):
    items = Carts.objects.filter(userId=user_id)
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)


# ======================================================
# ORDER
# ======================================================
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-date")
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# CATEGORY
# ======================================================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("CategoryName")
    serializer_class = CategorySerializer


# ======================================================
# LOCATION
# ======================================================
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("-id")
    serializer_class = LocationSerializer


@api_view(["POST"])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Location saved!", "data": serializer.data},
            status=201,
        )
    return Response(serializer.errors, status=400)


# ======================================================
# TABLE
# ======================================================
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# TABLE BOOKING
# ======================================================
class TableBookingViewSet(viewsets.ModelViewSet):
    queryset = TableBooking.objects.all().order_by("-created_at")
    serializer_class = TableBookingSerializer


# ======================================================
# RESERVATION (FIXED FOR MANY-TO-MANY)
# ======================================================
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Create reservation with multiple tables.
        """
        serializer.save()
