from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def limit_user_sessions(user, max_sessions=5):
    tokens = OutstandingToken.objects.filter(user=user).order_by('-created_at')

    if tokens.count() >= max_sessions:
        extra_tokens = tokens[max_sessions - 1:]   # keep space for new login
        channel_layer = get_channel_layer()

        for token in extra_tokens:
            try:
                refresh = RefreshToken(token.token)
                device_id = refresh.get("device_id", None)
            except Exception:
                device_id = None

            # 🔥 realtime logout
            if device_id:
                async_to_sync(channel_layer.group_send)(
                    f"user_{user.id}_{device_id}",
                    {
                        "type": "session_killed",
                    }
                )

            # 🔥 blacklist
            BlacklistedToken.objects.get_or_create(token=token)
            token.delete()