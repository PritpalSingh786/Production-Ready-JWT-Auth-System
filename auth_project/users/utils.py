from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .tasks import send_session_killed_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def limit_user_sessions(user, max_sessions=5, current_device_id=None):
    tokens = OutstandingToken.objects.filter(user=user).order_by('-created_at')

    if tokens.count() > max_sessions:
        extra_tokens = tokens[max_sessions:]
        channel_layer = get_channel_layer()

        for token in extra_tokens:
            device_id = token.payload.get("device_id")

            if device_id == current_device_id:
                continue

            # 🔥 REAL-TIME EVENT
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_{device_id}",
                {
                    "type": "session_killed",
                }
            )

            send_session_killed_email.delay(user.email)
            BlacklistedToken.objects.get_or_create(token=token)
            token.delete()