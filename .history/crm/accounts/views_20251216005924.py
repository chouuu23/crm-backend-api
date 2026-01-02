from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view

from .models import (
    User, Banner, Products, Cart, Receipt, Order,
    Category, Location, TableBooking, Table, Reservation
)

from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ProductSerializer, CartSerializer,
    ReceiptSerializer, OrderSerializer, CategorySerializer,
    LocationSerializer, TableBookingSerializer, TableSerializer,
    ReservationSerializer, BannerSerializer,
    SessionCartItemSerializer
)

from rest_framework.generics import ListAPIView
from .table_service import available_tables
from django.contrib.auth import authenticate




@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)

    if user is not None:
        return Response({
            "id": user.id,
            "name": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

    return Response(
        {"errors": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
def get_cart(request, user_id):
    carts = Cart.objects.filter(userId=user_id)

    data = []
    for c in carts:
        data.append({
            "cartId": c.cartId,
            "userId": c.userId,
            "productId": c.productId,
            "name": c.name,
            "price": float(c.price),
            "qty": c.qty,
            "img": c.img.url if c.img else ""
        })

    return Response(data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Carts, Products

@api_view(["POST"])
def place_order(request):
    user_id = request.data.get("user_id")
    items = request.data.get("items", [])

    if not user_id or not items:
        return Response(
            {"error": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not product_id or not quantity:
            continue

        # get product info
        product = Products.objects.get(id=product_id)

        # ✅ APPEND OR UPDATE (NO DELETE)
        cart, created = Carts.objects.get_or_create(
            userId=user_id,
            productId=product_id,
            defaults={
                "name": product.name,
                "price": product.price,
                "qty": quantity,
                "img": product.image,
            }
        )

        if not created:
            cart.qty += quantity
            cart.save()

    return Response(
        {"message": "Cart saved successfully"},
        status=status.HTTP_201_CREATED
    )


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        items = request.data.get("items", [])

        user = User.objects.get(id=user_id)

        for item in items:
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                product_id=item["product_id"],
                defaults={"quantity": item["quantity"]},
            )

            if not created:
                cart_item.quantity += item["quantity"]
                cart_item.save()

        return Response(
            {"message": "Cart updated"},
            status=status.HTTP_201_CREATED
        )




# ======================================================
# BASIC TEST VIEWS
# ======================================================

def home(request):
    return HttpResponse("Home_page")

def products(request):
    return HttpResponse("Products_page")

def customer(request):
    return HttpResponse("Customer_page")


# ======================================================
# BANNERS
# ======================================================

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


# ======================================================
# TABLE AVAILABILITY
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
# SESSION CART HELPERS (FLUTTER WEB SAFE)
# ======================================================

def _get_session_cart(request):
    return request.session.get("cart", [])

def _save_session_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


# ======================================================
# SESSION CART API (USED BY FLUTTER WEB)
# ======================================================

@api_view(["GET"])
def session_cart_get(request):
    return Response(_get_session_cart(request))


@api_view(["POST"])
def session_cart_add(request):
    serializer = SessionCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    item = serializer.validated_data

    cart = _get_session_cart(request)

    for c in cart:
        if c["id"] == item["id"]:
            c["quantity"] += item["quantity"]
            _save_session_cart(request, cart)
            return Response(cart)

    cart.append(item)
    _save_session_cart(request, cart)
    return Response(cart)


@api_view(["POST"])
def session_cart_decrease(request):
    item_id = request.data.get("id")
    cart = _get_session_cart(request)

    for c in cart:
        if c["id"] == item_id:
            if c["quantity"] > 1:
                c["quantity"] -= 1
            else:
                cart.remove(c)
            break

    _save_session_cart(request, cart)
    return Response(cart)


@api_view(["POST"])
def session_cart_clear(request):
    request.session["cart"] = []
    request.session.modified = True
    return Response({"success": True})


# ======================================================
# REGISTER
# ======================================================

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
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
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)


# ======================================================
# USER VIEWSET
# ======================================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-userId")
    serializer_class = UserSerializer


# ======================================================
# PRODUCT VIEWSET
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
# CART (DATABASE CART – NOT USED BY FLUTTER WEB)
# ======================================================
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("-id")
    serializer_class = CartSerializer


# ======================================================
# ORDER VIEWSET
# ======================================================

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-date")
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
# RECEIPT VIEWSET
# ======================================================

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by("-created_at")
    serializer_class = ReceiptSerializer


# ======================================================
# CATEGORY VIEWSET
# ======================================================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("categoryName")
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
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# ======================================================
# TABLE BOOKING
# ======================================================

class TableBookingViewSet(viewsets.ModelViewSet):
    queryset = TableBooking.objects.all()
    serializer_class = TableBookingSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
