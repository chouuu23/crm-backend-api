from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Users
from .serializers import UserSerializer


def home(request):
    return HttpResponse('Home_page')


def products(request):
    return HttpResponse('Products_page')


def customer(request):
    return HttpResponse('Customer_page')


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('userId')
    serializer_class = UserSerializer

from rest_framework import viewsets
from .models import Products
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('productId')
    serializer_class = ProductSerializer


