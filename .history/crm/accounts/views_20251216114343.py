from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view

from .models import (
    User, Banner, Products, Carts, Receipt, Order,
    Category, Location, TableBooking, Table, Reservation,Payment
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



@api_view(["PATCH"])
def pay_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id=booking_id)

    method = request.data.get("payment_method")
    amount = request.data.get("amount")

    # update booking
    booking.payment_method = method
    booking.payment_status = "Paid"
    booking.save()

    # create payment record
    Payment.objects.create(
        booking=booking,
        amount=amount,
        method=method.upper(),
        status="PAID",
    )

    return Response({"success": True})


@api_view(["GET"])
def payment_history(request, user_id):
    payments = Payment.objects.filter(
        booking__user_id=user_id
    ).order_by("-created_at")

    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)





@api_view(['PATCH'])
def mark_booking_paid(request, booking_id):
    try:
        booking = TableBooking.objects.get(id=booking_id)
    except TableBooking.DoesNotExist:
        return Response(
            {"error": "Booking not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    booking.payment_method = request.data.get("payment_method", "aba")
    booking.payment_status = "paid"
    booking.save()

    return Response(
        {"message": "Payment marked as paid"},
        status=status.HTTP_200_OK
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
    queryset = Carts.objects.all().order_by("-cartId")
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
