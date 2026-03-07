from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils.decorators import method_decorator

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": "User registered. Check your email."},
            status=status.HTTP_201_CREATED
        )
    

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response(
                {"error": "Invalid link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({"msg": "Email verified successfully"})

        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST
        )
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save(request)

        response = Response({"access": data["access"]})

        # Web → Refresh token in HttpOnly Cookie
        if data["platform"] == "web":
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=False,   # True in production
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )
        # Mobile → Refresh token in body
        else:
            response.data["refresh"] = data["refresh"]

        return response
    

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        # Web → Cookie
        if request.data.get("platform") == "web":
            refresh_token = request.COOKIES.get("refresh_token")
        else:
            refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RefreshTokenSerializer(
            data={
                "refresh": refresh_token,
                "platform": request.data.get("platform")
            }
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        response = Response({"access": data["access"]})

        # Web → Set new refresh in cookie
        if request.data.get("platform") == "web":
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=False,  # True in production
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )
        else:
            response.data["refresh"] = data["refresh"]

        return response
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        if request.data.get("platform") == "web":
            refresh_token = request.COOKIES.get("refresh_token")
        else:
            refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response({"msg": "Logout successful"})

        if request.data.get("platform") == "web":
            response.delete_cookie("refresh_token")

        return response
    

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": "If account exists, email sent"},
            status=status.HTTP_200_OK
        )


class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": "Password reset successful"},
            status=status.HTTP_200_OK
        )


class AuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "msg": "Welcome to authenticated view",
            "user": request.user.email
        })
    

