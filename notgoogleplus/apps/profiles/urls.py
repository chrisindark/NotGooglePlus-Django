from django.conf.urls import include, url

# from rest_framework import routers

from .views import *


# router = routers.SimpleRouter()
# router.register(r'profiles', ProfileViewSet)

urlpatterns = (
    url(r'profiles/$', ProfileListView.as_view(), name='account-profile-list'),
    url(r'profiles/(?P<user__username>[^/.]+)/$', ProfileDetailView.as_view(),
        name='account-profile-detail'),
    url(r'profiles/(?P<user__username>[^/.]+)/follow/$', ProfileFollowView.as_view(),
        name='account-profile-follow'),
)
