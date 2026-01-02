from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view

from .models import (
    User, Banner, Products, Carts, Receipt, Order,
    Category, Location, TableBooking, Table
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, CartSerializer,
    ReceiptSerializer, OrderSerializer,
    CategorySerializer, LocationSerializer,
    TableBookingSerializer, TableSerializer
)

# ------------------------------------------------------
# BASIC TEST VIEWS
# ------------------------------------------------------
def home(request):
    return HttpResponse('Home_page')


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
# CART VIEWSET (ADMIN / CRUD)
# ------------------------------------------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all().order_by('-cartId')
    serializer_class = CartSerializer


# ======================================================
# 🔥 CART PERSISTENCE FOR FLUTTER (IMPORTANT)
# ======================================================

@api_view(["GET"])
def get_user_cart(request):
    """
    GET /cart/user/?userId=1
    """
    user_id = request.GET.get("userId")

    if not user_id:
        return Response({"error": "userId required"}, status=400)

    cart_items = Carts.objects.filter(userId=user_id)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def save_user_cart(request):
    """
    POST /cart/save/
    {
      "userId": 1,
      "items": [
        {
          "productId": 2,
          "name": "Burger",
          "price": 3.5,
          "quantity": 2
        }
      ]
    }
    """
    user_id = request.data.get("userId")
    items = request.data.get("items", [])

    if not user_id:
        return Response({"error": "userId required"}, status=400)

    # Remove old cart
    Carts.objects.filter(userId=user_id).delete()

    # Save new cart
    for item in items:
        Carts.objects.create(
            userId=user_id,
            productId=item["productId"],
            name=item["name"],
            price=item["price"],
            qty=item["quantity"],
        )

    return Response({"status": "cart saved"})


# ------------------------------------------------------
# ORDER VIEWSET
# ------------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------------------------------------
# LOCATION
# ------------------------------------------------------
@api_view(['POST'])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location saved!", "data": serializer.data})
    return Response(serializer.errors, status=400)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('-id')
    serializer_class = LocationSerializer


# ------------------------------------------------------
# TABLE BOOKING
# ------------------------------------------------------
class TableBookingViewSet(viewsets.ModelViewSet):
    queryset = TableBooking.objects.all()
    serializer_class = TableBookingSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('number')
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]
