from django.conf.urls import url

# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    AccountListCreateView, AccountDetailView,
    LoginView, LogoutView, AccountActivateView,
    AccountConfirmView, AuthenticatedAccountView,
    JWTView, PasswordChangeView, PasswordResetView,
    PasswordResetConfirmView, GoogleOauthCallbackView,
    TwitterOauthView, TwitterOauthCallbackView,
)


# router = routers.SimpleRouter()
# router.register(r'accounts', AccountViewSet)

urlpatterns = (
    url(r'accounts/$', AccountListCreateView.as_view(), name='account-create'),
    url(r'accounts/(?P<pk>[0-9]+)/$', AccountDetailView.as_view(), name='account-detail'),

    # url(r'', include(router.urls)),

    url(r'auth/login/$', LoginView.as_view(), name='login'),
    url(r'auth/logout/$', LogoutView.as_view(), name='logout'),

    url(r'auth/account/activate/$', AccountActivateView.as_view(), name='account-activate'),
    url(r'auth/account/activate/confirm/$', AccountConfirmView.as_view(), name='account-confirm'),

    url(r'auth/password/change/$', PasswordChangeView.as_view(), name='password-change'),
    url(r'auth/password/reset/$', PasswordResetView.as_view(), name='password-reset'),
    url(r'auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'),

    url(r'auth/me/$', AuthenticatedAccountView.as_view(), name='account-me'),

    url(r'auth/google/callback/$', GoogleOauthCallbackView.as_view(), name='google-oauth-callback'),
    # url(r'auth/github/callback/$', GithubOauthCallbackView.as_view(), name='github-oauth-callback'),
    url(r'auth/twitter/$', TwitterOauthView.as_view(), name='twitter-oauth'),
    url(r'auth/twitter/callback/$', TwitterOauthCallbackView.as_view(), name='twitter-oauth-callback'),

    url(r'auth/jwt/login/$', JWTView.as_view(), name='jwt'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
