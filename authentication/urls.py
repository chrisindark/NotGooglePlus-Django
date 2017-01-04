from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

# router = routers.SimpleRouter()
# router.register(r'accounts', AccountViewSet)

urlpatterns = (
    url(r'^', include('django.contrib.auth.urls')),
    # url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/accounts/$', AccountCreateView.as_view(), name='account-create'),
    url(r'^api/v1/accounts/(?P<pk>[^/.]+)/$', AccountDetailView.as_view(), name='account-detail'),
    url(r'^api/v1/profiles/$', AccountProfileListView.as_view(), name='account-profile-list'),
    url(r'^api/v1/profiles/(?P<user__username>[^/.]+)/$', AccountProfileDetailView.as_view(), name='account-profile-detail'),
    # url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/login/$', obtain_auth_token, name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/auth/password/change/$', PasswordChangeView.as_view(), name='password-change'),
    url(r'^api/v1/auth/password/reset/$', PasswordResetView.as_view(), name='password-reset'),
    url(r'^api/v1/auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    url(r'^api/v1/auth/me/$', AuthenticatedUserView.as_view(), name='account-me'),

    # url('^.*$', IndexView.as_view(), name='index'),
)
