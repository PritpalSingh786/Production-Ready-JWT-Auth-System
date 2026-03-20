import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async
from .models import User, Device

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = None

        if "token=" in query_string:
            token = query_string.split("token=")[1]

        scope["user"] = AnonymousUser()
        scope["device_id"] = None

        if token:
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await sync_to_async(User.objects.get)(id=decoded["user_id"])

                # 🔥 device पहचान (User-Agent based)
                device = await sync_to_async(Device.objects.filter(
                    user=user,
                    device_name=scope["headers"]
                ).first)()

                scope["user"] = user
                scope["device_id"] = decoded.get("device_id")

            except Exception:
                pass

        return await super().__call__(scope, receive, send)