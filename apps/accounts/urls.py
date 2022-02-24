from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import routers

from .views import (
    AccountListCreateView, AccountDetailView, JWTLoginView,
    LoginView, LogoutView, AccountActivateView,
    AccountConfirmView, AuthenticatedAccountView,
    PasswordChangeView, PasswordResetView,
    PasswordResetConfirmView, GoogleOauthCallbackView,
    TwitterOauthView, TwitterOauthCallbackView,
)


# router = routers.SimpleRouter()
# router.register('accounts', AccountViewSet)

urlpatterns = (
    # path('', include(router.urls)),

    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/',
         AccountDetailView.as_view(), name='account-detail'),

    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    #     path('auth/account/activate/',
    #          AccountActivateView.as_view(), name='account-activate'),
    #     path('auth/account/activate/confirm/',
    #          AccountConfirmView.as_view(), name='account-confirm'),

    #     path('auth/password/change/',
    #          PasswordChangeView.as_view(), name='password-change'),
    #     path('auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
    #     path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(),
    #          name='password-reset-confirm'),

    path('auth/me/', AuthenticatedAccountView.as_view(), name='account-me'),

    #     path('auth/google/callback/', GoogleOauthCallbackView.as_view(),
    #         name='google-oauth-callback'),
    #     path('auth/twitter/', TwitterOauthView.as_view(), name='twitter-oauth'),
    #     path('auth/twitter/callback/', TwitterOauthCallbackView.as_view(),
    #         name='twitter-oauth-callback'),
    #     path('auth/github/callback/', GithubOauthCallbackView.as_view(), name='github-oauth-callback'),

    path('auth/jwt/login/', JWTLoginView.as_view(), name='jwt-login'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
