from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view

from .models import (
    Banner, Products, Carts, Receipt, Order,
    Category, Location, TableBooking, Table, Reservation, Payment
)


from .serializers import (
    PaymentSerializer,
    RegisterSerializer,
    ProductSerializer,
    CartSerializer,
    ReceiptSerializer,
    OrderSerializer,
    CategorySerializer,
    LocationSerializer,
    TableBookingSerializer,
    TableSerializer,
    ReservationSerializer,
    BannerSerializer,
    SessionCartItemSerializer,
)




from rest_framework.generics import ListAPIView
from .table_service import available_tables




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TableBooking, Payment
from .serializers import PaymentSerializer




from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class JWTLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Email is used as username
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "name": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK
        )
class JWTLoginView(APIView):
    permission_classes = [permissions.AllowAny]
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

# @api_view(["PATCH"])
# def pay_booking(request, booking_id):
#     try:
#         booking = TableBooking.objects.get(id=booking_id)
#     except TableBooking.DoesNotExist:
#         return Response(
#             {"error": "Booking not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     payment, created = Payment.objects.get_or_create(
#         booking=booking,
#         defaults={
#             "amount": request.data.get("amount"),
#             "method": request.data.get("method"),
#             "status": "PAID",
#         }
#     )

#     if not created:
#         payment.amount = request.data.get("amount", payment.amount)
#         payment.method = request.data.get("method", payment.method)
#         payment.status = request.data.get("status", "PAID")

#     payment.save()

#     serializer = PaymentSerializer(payment)
#     return Response(serializer.data, status=status.HTTP_200_OK)



# from django.http import JsonResponse
# from .models import Payment

# def payment_history(request, user_id):
#     payments = (
#         Payment.objects
#         .select_related("booking", "booking__user")
#         .filter(booking__user=user_id)   # ✅ FIX HERE
#         .order_by("method", "-created_at")
#     )

#     data = [
#         {
#             "id": p.id,
#             "amount": float(p.amount),
#             "method": p.method,
#             "status": p.status,
#             "transaction_id": p.transaction_id,
#             "created_at": p.created_at.isoformat(),
#         }
#         for p in payments
#     ]

#     return JsonResponse(data, safe=False)


# views.py
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Payment
# from .serializers import PaymentSerializer

# @api_view(['GET'])
# def payment_history(request, user_id):
#     payments = (
#         Payment.objects
#         .select_related("booking", "booking__user")
#         .filter(booking__user__id=user_id)
#         .order_by("method", "-created_at")
#     )
    
#     serializer = PaymentSerializer(payments, many=True)
#     return Response(serializer.data)


# @api_view(['PATCH'])
# def mark_booking_paid(request, booking_id):
#     try:
#         booking = TableBooking.objects.get(id=booking_id)
#     except TableBooking.DoesNotExist:
#         return Response(
#             {"error": "Booking not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     # ✅ Update booking
#     booking.payment_method = request.data.get("method", "ABA")
#     booking.payment_status = "PAID"
#     booking.save()

#     # ✅ Create payment record
#     payment = Payment.objects.create(
#         booking=booking,
#         amount=request.data.get("amount"),
#         method=request.data.get("method", "ABA"),
#         status="PAID",
#     )

#     # ✅ Serialize payment
#     serializer = PaymentSerializer(payment)

#     # ✅ Return payment JSON (IMPORTANT)
#     return Response(serializer.data, status=status.HTTP_200_OK)

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

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data)
#         return Response(serializer.errors, status=400)


# ======================================================
# USER VIEWSET
# ======================================================


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
    serializer_class = TableBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TableBooking.objects.filter(user=self.request.user)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Payment
from .serializers import PaymentSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    # 🔐 USER CAN ONLY SEE THEIR OWN PAYMENTS
    def get_queryset(self):
        return (
            Payment.objects
            .select_related("booking")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    # ❌ BLOCK DUPLICATE PAYMENTS
    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")

        booking = get_object_or_404(
            TableBooking,
            id=booking_id,
            user=request.user
        )

        if hasattr(booking, "payment"):
            return Response(
                {"error": "Payment already exists for this booking"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    # ✅ CONFIRM PAYMENT
    @action(detail=True, methods=["patch"])
    def pay(self, request, pk=None):
        payment = self.get_object()

        if payment.status == "PAID":
            raise PermissionDenied("Payment already completed")

        payment.status = "PAID"
        payment.transaction_id = request.data.get("transaction_id")
        payment.save()

        # Update booking status
        booking = payment.booking
        booking.payment_status = "paid"
        booking.payment_method = payment.method
        booking.save()

        serializer = self.get_serializer(payment)
        return Response(serializer.data)



# View a single payment by ID
# GET /api/payments/single/<pk>/

# @api_view(['GET'])
# def payment_detail(request, pk):
#     payment = get_object_or_404(Payment, pk=pk)
#     serializer = PaymentSerializer(payment)
#     return Response(serializer.data)

# -----------------------------
# View payments by user ID
# GET /api/payments/user/<user_id>/
# -----------------------------

# GET /api/payments/user/<user_id>/
# @api_view(['GET'])
# def payments_by_user(request, user_id):
#     # ទាញ booking id របស់អ្នកប្រើ
#     booking_ids = TableBooking.objects.filter(user__id=user_id).values_list('id', flat=True)

#     # ទាញ payment ដែលមាន booking id
#     payments = Payment.objects.filter(booking_id__in=booking_ids).order_by('-created_at')

#     serializer = PaymentSerializer(payments, many=True)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def payment_update(request, pk):
#     payment = get_object_or_404(Payment, pk=pk)
#     serializer = PaymentSerializer(payment, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# def payment_delete(request, pk):
#     payment = get_object_or_404(Payment, pk=pk)
#     payment.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
