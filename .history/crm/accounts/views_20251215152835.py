from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

from .models import (
    Banner,
    Products,
    Carts,
    Receipt,
    Order,
    Category,
    Location,
    Table,
    Reservation,
)

from .serializers import (
    BannerSerializer,
    ProductSerializer,
    CartSerializer,
    ReceiptSerializer,
    OrderSerializer,
    CategorySerializer,
    LocationSerializer,
    TableSerializer,
    ReservationSerializer,
    LoginSerializer,
    UserSerializer,
)

from .table_service import available_tables


# ======================================================
# BASIC TEST VIEWS
# ======================================================
def home(request):
    return HttpResponse("Home_page")


# ======================================================
# BANNERS
# ======================================================
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


# ======================================================
# TABLE AVAILABILITY (CUSTOM API)
# ======================================================
@api_view(["GET"])
def tables_api(request):
    date = request.GET.get("date")
    time = request.GET.get("time")
    seats = request.GET.get("seats")

    if not (date and time and seats):
        return Response(
            {"error": "date, time, and seats are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tables = available_tables(date, time, int(seats))
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


# ======================================================
# AUTH
# ======================================================
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "Login successful", "data": serializer.validated_data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================================
# PRODUCTS
# ======================================================
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Products.objects.all().order_by("-productId")
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


# ======================================================
# CART (USER BASED)
# ======================================================
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get("userId")
        if not user_id:
            return Carts.objects.none()
        return Carts.objects.filter(user_id=user_id)

    @action(detail=False, methods=["post"])
    def add(self, request):
        user_id = request.data.get("userId")
        product_id = request.data.get("productId")

        if not user_id or not product_id:
            return Response(
                {"error": "userId and productId are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item, created = Carts.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults={"qty": 1},
        )

        if not created:
            item.qty += 1
            item.save()

        return Response({"success": True})


# ======================================================
# ORDERS
# ======================================================
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# CATEGORIES
# ======================================================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("categoryName")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# LOCATION
# ======================================================
@api_view(["POST"])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location saved", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("-created_at")
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# TABLES
# ======================================================
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# RESERVATIONS (FINAL, CORRECT)
# ======================================================
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        tables = serializer.validated_data["tables"]
        date = serializer.validated_data["date"]
        time = serializer.validated_data["time"]

        for table in tables:
            if Reservation.objects.filter(
                tables=table, date=date, time=time
            ).exists():
                raise ValidationError(
                    f"Table {table.number} is already reserved at this time."
                )

        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)
