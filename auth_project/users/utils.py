from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .tasks import send_session_killed_email

def limit_user_sessions(user, max_sessions=5):
    # 🔥 newest → oldest
    tokens = OutstandingToken.objects.filter(user=user).order_by('-created_at')

    # agar limit exceed ho gayi
    if tokens.count() > max_sessions:
        extra_tokens = tokens[max_sessions:]

        for token in extra_tokens:
            # 🔥 Send notification
            send_session_killed_email.delay(user.email)
            
            # 🔐 blacklist
            BlacklistedToken.objects.get_or_create(token=token)

            # 🧹 delete
            token.delete()