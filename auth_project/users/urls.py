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
🔐 Final Secure Flow (Your Case)
Step	Action
1	Register → Email Verify
2	Login → Access + Refresh
3	Refresh Token → Rotated
4	Old Refresh → Blacklisted
5	Logout → Manual Blacklist  

✔ A stolen refresh token cannot be reused
✔ After logout, the token becomes invalid
✔ Refresh token rotation increases the security level
✔ Production-ready setup
✔ Enterprise-grade implementation

web: gunicorn rentNotify.wsgi
worker: celery -A auth_project worker --loglevel=info
beat:  celery -A auth_project beat -l info


Sure 😎, short version in English:

---

**Why storing JWT in cookies is safer than localStorage:**

1. **HttpOnly:** JS cannot access the cookie → safe from XSS attacks.
2. **Secure:** Cookie sent only over HTTPS → safe from network sniffing.
3. **SameSite:** Protects against CSRF → cookie not sent on cross-site requests.
4. **Auto-send:** Browser sends cookies automatically with requests (`credentials: "include"`).
5. **Short-lived access token + HttpOnly refresh token:** Even if leaked, access token expires quickly.

**Compare:**

| Feature       | LocalStorage | HttpOnly Cookie |
| ------------- | ------------ | --------------- |
| JS access     | ✅ Yes        | ❌ No            |
| XSS safe      | ❌ No         | ✅ Yes           |
| CSRF safe     | ❌ No         | ✅ Yes           |
| Auto send req | ❌ No         | ✅ Yes           |

**✅ Conclusion:** Cookies with `HttpOnly`, `Secure`, and `SameSite` + short-lived tokens are the safest way to store JWT in the browser.


'''