from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView, Response, status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from .models import (
    User, Products, SlideShow, Carts, Receipt, Order, Category, Location
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, SlideShowSerializer, CartSerializer,
    ReceiptSerializer, OrderSerializer, CategorySerializer,
    LocationSerializer
)


# app/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Receipt
from .serializers import ReceiptSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners may modify; read-only is allowed for safe methods.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permitted for anyone (you can limit to authenticated if desired)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD for Receipt.
    - list: returns receipts of authenticated user
    - create: sets request.user as owner
    - retrieve: allowed for owner
    - update/partial_update/destroy: owner only
    Extra action:
    POST /receipts/{pk}/mark_paid/  -> marks the receipt as paid
    """
    queryset = Receipt.objects.all().select_related("user").prefetch_related("items")
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Limit to current user's receipts
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return Receipt.objects.none()

    def perform_create(self, serializer):
        # Ensure the owner is set to request.user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="mark_paid")
    def mark_paid(self, request, pk=None):
        receipt = get_object_or_404(self.get_queryset(), pk=pk)
        # Permission check via IsOwnerOrReadOnly implicitly applied earlier
        receipt.is_paid = True
        receipt.save()
        return Response({"status": "marked as paid"}, status=status.HTTP_200_OK)




# ------------------- LOCATION SAVE (POST only) -------------------
@api_view(['POST'])
def save_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location saved!", "data": serializer.data})
    return Response(serializer.errors, status=400)


# ------------------- LOCATION VIEWSET (CRUD) -------------------
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# -------------------- BASIC TEST VIEWS --------------------
def home(request):
    return HttpResponse('Home_page')

def products(request):
    return HttpResponse('Products_page')

def customer(request):
    return HttpResponse('Customer_page')


# ------------------------ REGISTER ------------------------
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


# ------------------------ LOGIN ------------------------
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


# ------------------------ USER ------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -------------------- PRODUCT --------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Products.objects.all().order_by('-productId')
        category_id = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


# -------------------- SLIDE SHOW --------------------
class SlideShowViewSet(viewsets.ModelViewSet):
    queryset = SlideShow.objects.all().order_by('ID')
    serializer_class = SlideShowSerializer


# -------------------- CART --------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all().order_by('userId')
    serializer_class = CartSerializer


# -------------------- RECEIPT --------------------
class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('receiptId')
    serializer_class = ReceiptSerializer


# -------------------- ORDER --------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# -------------------- CATEGORY --------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('CategoryName')
    serializer_class = CategorySerializer
