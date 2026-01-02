from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action

from .models import (
    User, Products, SlideShow, Carts, MyReceipt, Order, Category, Location
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, SlideShowSerializer, CartSerializer,
    ReceiptSerializer, OrderSerializer, CategorySerializer,
    LocationSerializer
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
    queryset = MyReceipt.objects.all().order_by('-date')
    serializer_class = MyReceiptSerializer

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
    queryset = Location.objects.all().order_by('-created_at')
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


# ------------------------------------------------------
# CATEGORY VIEWSET
# ------------------------------------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('CategoryName')
    serializer_class = CategorySerializer
