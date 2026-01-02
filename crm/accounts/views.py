from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Count, Sum, Avg

from .models import Payment
from .serializers import PaymentSerializer

from rest_framework.decorators import action


from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from .models import Cart
from .serializers import CartSerializer

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Payment
from .serializers import PaymentSerializer
from accounts.models import TableBooking


from .models import (
    Banner, Products, Cart, Receipt, Order,
    Category, Location, TableBooking, Table, Reservation, Payment, Favorite
)


from .serializers import (
    PaymentSerializer,
    
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
    FavoriteSerializer,
)




from rest_framework.generics import ListAPIView
from .table_service import available_tables




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TableBooking, Payment
from .serializers import PaymentSerializer



from django.contrib.auth.hashers import check_password

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()





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
    permission_classes = [AllowAny]


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_decrease(request):
    product_id = request.data.get("product_id")

    cart = Cart.objects.filter(
        user=request.user,
        product_id=product_id
    ).first()

    if not cart:
        return Response({"detail": "Item not found"}, status=404)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return Response({"success": True})

# ======================================================
# PRODUCT VIEWSET
# ======================================================

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]   # ✅ THIS FIXES 401
    queryset = Products.objects.all() 
    def get_queryset(self):
        queryset = Products.objects.all().order_by("-productId")
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

# ======================================================
# Fav
# ======================================================
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("FAVORITE API USER:", user.username)
        return Favorite.objects.filter(user=user)


    def perform_create(self, serializer):
        serializer.save()
   
        

# ======================================================
# CART (DATABASE CART – NOT USED BY FLUTTER WEB)
# ======================================================

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all() 
    def get_queryset(self):
        return (
            Cart.objects
            .select_related("product")
            .filter(user=self.request.user)
            .order_by("-id")
        )

    def get_serializer_context(self):
        return {"request": self.request}

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









class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "total_products": Products.objects.count(),
            "total_sales": (
                Payment.objects.filter(status="PAID")
                .aggregate(total=Sum("amount"))["total"] or 0
            ),
            "total_bookings": TableBooking.objects.count(),
        })


class AdminRecentBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        bookings = TableBooking.objects.order_by("-created_at")[:5]
        return Response([
            {
                "id": b.id,
                "customer_name": b.customer_name,
                "date": b.date,
                "time": b.time,
                "guests": b.guests,
                "payment_status": b.payment_status,
            }
            for b in bookings
        ])


class AdminRecentPaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        payments = Payment.objects.order_by("-created_at")[:5]
        return Response([
            {
                "booking_id": p.booking.id,
                "customer": p.booking.customer_name,
                "amount": p.amount,
                "method": p.method,
                "status": p.status,
                "created_at": p.created_at,
            }
            for p in payments
        ])
    


User = get_user_model()

class AdminUserListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by("-date_joined")
        data = []

        for u in users:
            data.append({
                "id": u.id,
                "name": u.username,
                "email": u.email,
                "role": "Admin" if u.is_staff else "Customer",
                "status": "Active" if u.is_active else "Inactive",
                "joined": u.date_joined.strftime("%Y-%m-%d"),
            })

        return Response(data)


class AdminPaymentListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        payments = Payment.objects.select_related("booking").order_by("-created_at")

        data = []
        for p in payments:
            data.append({
                "id": p.id,
                "booking_id": p.booking.id if p.booking else None,
                "amount": float(p.amount),
                "method": p.method,
                "status": p.status,
                "created_at": p.created_at.isoformat(),
            })

        return Response(data)
    


class AdminBookingListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bookings = TableBooking.objects.order_by("-created_at")

        data = []
        for b in bookings:
            data.append({
                "id": b.id,
                "customer_name": b.customer_name or "—",
                "guests": b.guests,
                "date": b.date.strftime("%Y-%m-%d"),
                "time": b.time.strftime("%H:%M"),
                "payment_status": b.payment_status,
            })

        return Response(data)
    

class AdminProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "full_name": user.get_full_name() or user.username,
            "email": user.email,
            "phone": getattr(user, "phone", ""),
            "role": "Super Admin" if user.is_superuser else "Admin"
        })
    


class BestSellingProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = (
            Products.objects
            .filter(isPopular=True)
            .order_by("-rating")[:5]
        )

        data = [
            {
                "productId": p.productId,
                "name": p.name,
                "price": p.price,
                "image": request.build_absolute_uri(p.image.url) if p.image else "",
                "category": str(p.category) if p.category else "",
                "rating": p.rating,
            }
            for p in products
        ]

        return Response(data)












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
    queryset = TableBooking.objects.all() 
    def get_queryset(self):
        return TableBooking.objects.filter(user=self.request.user)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    queryset = Payment.objects.all()

    def get_queryset(self):
        return (
            Payment.objects
            .select_related("booking")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

    # ================= CREATE PAYMENT =================
    def perform_create(self, serializer):
        booking_id = self.request.data.get("booking")

        booking = get_object_or_404(
            TableBooking,
            id=booking_id,
            user=self.request.user
        )

        if hasattr(booking, "payment"):
            raise ValidationError("Payment already exists for this booking")

        serializer.save(
            user=self.request.user,
            booking=booking
        )

    # ================= UPLOAD RECEIPT (STEP 3) =================
    @action(detail=True, methods=["post"], url_path="upload-receipt")
    def upload_receipt(self, request, pk=None):
        payment = self.get_object()

        # ❌ Prevent re-upload after approval
        if payment.approved_by_admin:
            raise PermissionDenied("Payment already approved")

        receipt = request.FILES.get("receipt")
        if not receipt:
            raise ValidationError({"receipt": "Receipt file is required"})

        payment.receipt = receipt
        payment.receipt_uploaded_at = timezone.now()
        payment.status = "PENDING"  # stays pending until admin approves
        payment.save()

        return Response(
            self.get_serializer(payment).data,
            status=status.HTTP_200_OK
        )

    # ================= CONFIRM PAYMENT =================
    @action(detail=True, methods=["patch"])
    def pay(self, request, pk=None):
        payment = self.get_object()

        # ❌ Must have receipt first
        if not payment.receipt:
            raise ValidationError("Upload receipt before confirming payment")

        # ❌ Prevent double payment
        if payment.status == "PAID":
            raise PermissionDenied("Payment already completed")

        payment.status = "PAID"
        payment.transaction_id = request.data.get("transaction_id")
        payment.save()

        booking = payment.booking
        booking.payment_status = "paid"
        booking.payment_method = payment.method
        booking.save()

        return Response(
            self.get_serializer(payment).data,
            status=status.HTTP_200_OK
        )
