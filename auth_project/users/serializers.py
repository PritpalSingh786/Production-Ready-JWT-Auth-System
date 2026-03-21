from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import Device
from .tasks import send_email_task
import datetime
import re
from .utils import limit_user_sessions
import uuid

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    # 🔹 Field-level validation for username
    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long")

        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can contain only letters, numbers and underscore"
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value

    # 🔹 Field-level validation for email
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    # 🔹 Object-level validation (optional extra checks)
    def validate(self, attrs):
        if len(attrs["password"]) < 6:
            raise serializers.ValidationError(
                {"password": "Password must be at least 6 characters long"}
            )
        return attrs

    # 🔹 Save method
    def save(self, **kwargs):
        user = User.objects.create_user(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            password=self.validated_data["password"]
        )

        # Email verification logic
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        message = f"Verify before {expire} UTC: {link}"
        send_email_task.delay("Verify Email", message, [user.email])

        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    platform = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.email_verified:
            raise serializers.ValidationError("Email not verified")

        attrs["user"] = user
        return attrs

    def save(self, request):
        user = self.validated_data["user"]
        # 🔥 session limit
        limit_user_sessions(user, max_sessions=5)

        # 🔥 device id generate
        device_id = str(uuid.uuid4())
        # 🔥 Step 1: new token create
        refresh = RefreshToken.for_user(user)

        # Custom payload in refresh
        refresh["device_id"] = device_id
        refresh["platform"] = self.validated_data["platform"]
        # ✅ add issuer & audience
        refresh["iss"] = "my-app"
        refresh["aud"] = "my-users"
        # refresh["userId"] = user.id
        # refresh["username"] = user.username
        # refresh["email"] = user.email


        access = refresh.access_token

        # Custom payload in access
        access["device_id"] = device_id
        access["userId"] = user.id
        access["iss"] = "my-app"
        access["aud"] = "my-users"
        access["platform"] = self.validated_data["platform"]
        # Never store PII (Personally Identifiable Info) in tokens 
        # use opque tokens outside
        # JWTs inside - also called split token or phantom token pattern 
        # access["username"] = user.username
        # access["email"] = user.email

        Device.objects.update_or_create(
            user=user,
            device_name=request.headers.get("User-Agent"),
            defaults={"ip_address": request.META.get("REMOTE_ADDR")}
        )

        return {
            "access": str(access),
            "refresh": str(refresh),
            "platform": self.validated_data["platform"]
        }
    

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)
    platform = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        if not refresh_token:
            raise serializers.ValidationError("Refresh token required")

        try:
            refresh = RefreshToken(refresh_token)
        except:
            raise serializers.ValidationError("Invalid refresh token")

        attrs["refresh_obj"] = refresh
        return attrs

    def save(self):
        refresh = self.validated_data["refresh_obj"]
        refresh.blacklist()

        new_refresh = RefreshToken.for_user(refresh.user)

        return {
            "access": str(new_refresh.access_token),
            "refresh": str(new_refresh)
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        self.user = User.objects.filter(email=attrs["email"]).first()
        return attrs

    def save(self):
        if not self.user:
            return

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        send_email_task.delay(
            "Reset Password",
            f"Reset before {expire} UTC: {link}",
            [self.user.email]
        )


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(pk=uid)
        except:
            raise serializers.ValidationError("Invalid link")

        if not token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()