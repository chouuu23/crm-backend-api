from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse('Home_page')

def products(request):
    return HttpResponse('Products_page')

def customer(request):
    return HttpResponse('Customer_page')  

from .models import TblUsers
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = TblUsers.objects.all().order_by('userId')
    serializer_class = UserSerializer
