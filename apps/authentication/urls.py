from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import JWTLoginView, LoginView, LogoutView

urlpatterns = (
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/jwt/", JWTLoginView.as_view(), name="login-jwt"),
    path("jwt/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
)
