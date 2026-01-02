from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Users
from .serializers import UserSerializer


from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .models import (Users,Products,SlideShow,Carts,Receipt,)

from .serializers import (UserSerializer,ProductSerializer,SlideShowSerializer,CartSerializer,ReceiptSerializer,)


def home(request):
    return HttpResponse('Home_page')


def products(request):
    return HttpResponse('Products_page')


def customer(request):
    return HttpResponse('Customer_page')




# -------------------- BASIC VIEWS --------------------
def home(request):
    return HttpResponse('Home_page')


def products(request):
    return HttpResponse('Products_page')


def customer(request):
    return HttpResponse('Customer_page')


# -------------------- USER --------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('userId')
    serializer_class = UserSerializer


# -------------------- PRODUCT --------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('productId')
    serializer_class = ProductSerializer


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

