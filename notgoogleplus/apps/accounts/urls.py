from django.conf.urls import url

# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

# router = routers.SimpleRouter()
# router.register(r'accounts', AccountViewSet)

urlpatterns = (
    # url(r'^api/v1/', include(router.urls)),
    url(r'accounts/$', AccountCreateView.as_view(), name='account-create'),
    url(r'accounts/(?P<pk>[0-9]+)/$', AccountDetailView.as_view(), name='account-detail'),

    url(r'auth/login/$', LoginView.as_view(), name='login'),
    url(r'auth/logout/$', LogoutView.as_view(), name='logout'),

    url(r'auth/account/activate/$', AccountActivateView.as_view(), name='account-activate'),
    url(r'auth/account/activate/confirm/$', AccountConfirmView.as_view(), name='account-confirm'),

    url(r'auth/password/change/$', PasswordChangeView.as_view(), name='password-change'),
    url(r'auth/password/reset/$', PasswordResetView.as_view(), name='password-reset'),
    url(r'auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'),

    url(r'auth/me/$', AuthenticatedAccountView.as_view(), name='account-me'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
