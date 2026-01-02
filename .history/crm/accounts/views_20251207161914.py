from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Users
from rest_framework import permissions

from .models import (Users,Products,SlideShow,Carts,Receipt,Order,Category)

from .serializers import (UserSerializer,ProductSerializer,SlideShowSerializer,CartSerializer,ReceiptSerializer,OrderSerializer,CategorySerializer)

# -------------------- BASIC VIEWS --------------------
def home(request):
    return HttpResponse('Home_page')


def products(request):
    return HttpResponse('Products_page')


def customer(request):
    return HttpResponse('Customer_page')


# -------------------- USER --------------------
class LoginrViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('userId')
    serializer_class = UserSerializer


# -------------------- PRODUCT --------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()   # IMPORTANT
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny] 

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('CategoryName')
    serializer_class = CategorySerializer