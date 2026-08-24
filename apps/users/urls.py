from django.urls import path

from apps.users.views import (
    AuthorizedUserView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserActivateView,
    UserActivationConfirmView,
    UserDestroyView,
    UserListCreateView,
    UserRetrieveDetailView,
    UserUpdateView,
)

urlpatterns = (
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path("<int:pk>/", UserRetrieveDetailView.as_view(), name="user-retrieve-detail"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyView.as_view(), name="user-delete"),
    path("me/", AuthorizedUserView.as_view(), name="user-me"),
    path("activate/", UserActivateView.as_view(), name="user-activate"),
    path(
        "activation/confirm/",
        UserActivationConfirmView.as_view(),
        name="user-activation-confirm",
    ),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("password/reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
)
