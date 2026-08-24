from django.urls import path

from .views import (
    AuthorizedProfileView,
    ProfileCreateView,
    ProfileDeleteView,
    ProfileListView,
    ProfileRetrieveDetailView,
    ProfileUpdateView,
)

urlpatterns = (
    path("", ProfileListView().as_view(), name="user-profile-list"),
    path("create/", ProfileCreateView().as_view(), name="user-profile-create"),
    path(
        "<int:pk>/",
        ProfileRetrieveDetailView().as_view(),
        name="user-profile-retrieve-detail",
    ),
    path(
        "<int:pk>/update/",
        ProfileUpdateView().as_view(),
        name="user-profile-update",
    ),
    path(
        "<int:pk>/delete/",
        ProfileDeleteView().as_view(),
        name="user-profile-delete",
    ),
    path("me/", AuthorizedProfileView().as_view(), name="user-profile-me"),
    # path('profiles/(?P<user__username>[^/.]+)/', ProfileDetailView().as_view(),
    # name='user-profile-detail'),
    # path('profiles/(?P<user__username>[^/.]+)/follow/', ProfileFollowView.as_view(),
    #     name='user-profile-follow'),
)
