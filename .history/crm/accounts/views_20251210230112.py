from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action

from .models import (
    User, Products, SlideShow, Carts, MyReceipt, Order, Category, Location,TableBooking,Table
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, SlideShowSerializer, CartSerializer,
    MyReceiptSerializer, OrderSerializer, CategorySerializer,
    LocationSerializer,TableBookingSerializer,TableSerializer
)


# ------------------------------------------------------
# PERMISSION: Only owner can modify
# ------------------------------------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners may modify; read-only is allowed for safe methods.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# ------------------------------------------------------
# RECEIPT VIEWSET (FINAL WORKING VERSION)
# ------------------------------------------------------
class MyReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = MyReceiptSerializer
    queryset = MyReceipt.objects.all().order_by('-date')

# ------------------------------------------------------
# LOCATION (Post only simple) - for saving address
# ------------------------------------------------------
@api_view(['POST'])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location saved!", "data": serializer.data})
    return Response(serializer.errors, status=400)


# ------------------------------------------------------
# LOCATION CRUD VIEWSET
# ------------------------------------------------------
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('-id')
    serializer_class = LocationSerializer


# ------------------------------------------------------
# BASIC TEST VIEWS
# ------------------------------------------------------
def home(request):
    return HttpResponse('Home_page')

def products(request):
    return HttpResponse('Products_page')

def customer(request):
    return HttpResponse('Customer_page')


# ------------------------------------------------------
# REGISTER
# ------------------------------------------------------
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "User registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)


# ------------------------------------------------------
# LOGIN
# ------------------------------------------------------
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                "status": 200,
                "message": "Login successful",
                "data": serializer.validated_data
            }, status=200)

        return Response({"errors": serializer.errors}, status=400)


# ------------------------------------------------------
# USER VIEWSET
# ------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-userId')
    serializer_class = UserSerializer


# ------------------------------------------------------
# PRODUCT VIEWSET
# ------------------------------------------------------
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Products.objects.all().order_by('-productId')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


# ------------------------------------------------------
# SLIDESHOW VIEWSET
# ------------------------------------------------------
class SlideShowViewSet(viewsets.ModelViewSet):
    queryset = SlideShow.objects.all().order_by('ID')
    serializer_class = SlideShowSerializer


# ------------------------------------------------------
# CART VIEWSET
# ------------------------------------------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all().order_by('-cartId')
    serializer_class = CartSerializer


# ------------------------------------------------------
# ORDER VIEWSET
# ------------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('-created_at')
    serializer_class = ReceiptSerializer


# ------------------------------------------------------
# CATEGORY VIEWSET
# ------------------------------------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('CategoryName')
    serializer_class = CategorySerializer

class TableBookingViewSet(viewsets.ModelViewSet):
    queryset = TableBooking.objects.all()
    serializer_class = TableBookingSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('number')
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]  # adjust to your auth policy


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('-created_at')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        When creating a reservation:
          - check table availability (unique_together helps, but we double-check)
          - mark the table as reserved
        """
        table = serializer.validated_data['table']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        # check for existing reservation for that table+date+time
        exists = Reservation.objects.filter(table=table, date=date, time=time).exists()
        if exists:
            raise serializers.ValidationError("This table is already reserved at that date/time.")

        # save reservation (attach request.user if available)
        user = self.request.user if self.request.user.is_authenticated else None
        # If you require user, ensure IsAuthenticated permission is set
        reservation = serializer.save(user=user)

        # mark table reserved (business rule — if you want per-slot reservation, you may not set is_reserved True globally)
        table.is_reserved = True
        table.save()

    def perform_destroy(self, instance):
        # When a reservation is deleted, optionally un-reserve the table (simple approach)
        table = instance.table
        instance.delete()
        # If there are no other reservations for this table at other times/dates, unreserve
        still_reserved = Reservation.objects.filter(table=table).exists()
        if not still_reserved:
            table.is_reserved = False
            table.save()