from django.urls import path
from .views import (RegisterView, VerifyEmailView, LoginView, RefreshTokenView, 
                    LogoutView, PasswordResetRequestView, SetNewPasswordView, AuthenticatedView)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailView.as_view()),
    path("login/", LoginView.as_view()),
    path("token/refresh/", RefreshTokenView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("request-password-reset/", PasswordResetRequestView.as_view()),
    path("reset-password/", SetNewPasswordView.as_view()),
    path("authenticated/", AuthenticatedView.as_view(), name="authenticated"),
]


'''

web: gunicorn rentNotify.wsgi
worker: celery -A auth_project worker --loglevel=info
beat:  celery -A auth_project beat -l info

'''