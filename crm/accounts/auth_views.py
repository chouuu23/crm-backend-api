from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile

User = get_user_model()


# ===================== ME =====================
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ✅ ALWAYS ENSURE PROFILE EXISTS
        profile = UserProfile.objects.filter(user=user).first()

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": profile.phone or "",
        })


# ===================== LOGIN =====================
class JWTLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")

        if not login or not password:
            return Response(
                {"error": "Email/Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=login)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            user = authenticate(username=login, password=password)
            if user is None:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        refresh = RefreshToken.for_user(user)

        # ✅ SAFE PROFILE ACCESS
        profile = UserProfile.objects.filter(user=user).first()


        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": profile.phone or "",
        })


# ===================== REGISTER =====================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not all([username, email, phone, password]):
            return Response(
                {"error": "All fields required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email exists"}, status=400)

        if UserProfile.objects.filter(phone=phone).exists():
            return Response({"error": "Phone exists"}, status=400)

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # CREATE PROFILE
        UserProfile.objects.create(
            user=user,
            phone=phone
        )

        return Response(
            {"message": "Registered successfully"},
            status=status.HTTP_201_CREATED
        )
