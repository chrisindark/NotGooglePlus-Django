import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from apps.profiles.models import Profile
from apps.users.mixins import ProfileMixin

from .permissions import IsProfileOwner
from .serializers import AuthorizedProfileSerializer

logger = logging.getLogger(__name__)


# Create your views here.
class ProfileListView(ProfileMixin, generics.ListAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    # filter_class = ProfileFilter


class ProfileCreateView(ProfileMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorizedProfileSerializer


class ProfileRetrieveDetailView(ProfileMixin, generics.RetrieveAPIView):
    # lookup_field = "user__username"

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return [
    #             permissions.AllowAny(),
    #         ]
    #     return [
    #         permissions.IsAuthenticated(),
    #         IsProfileOwner(),
    #     ]

    # def get_queryset(self):
    #     try:
    #         kwargs = {"username": self.kwargs.get(self.lookup_field)}
    #         user = User.objects.get(**kwargs)
    #         Profile.objects.get_or_create(user=user)
    #         queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
    #         return queryset
    #     except User.DoesNotExist:
    #         raise NotFound()
    pass


class ProfileUpdateView(ProfileMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    serializer_class = AuthorizedProfileSerializer


class ProfileDeleteView(ProfileMixin, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    serializer_class = AuthorizedProfileSerializer


class AuthorizedProfileView(ProfileMixin, generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsProfileOwner,
    ]
    serializer_class = AuthorizedProfileSerializer

    def get_object(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        return profile

    def get(self, request, *args, **kwargs):
        self.kwargs["pk"] = request.user.id
        logger.info(f"Retrieving authenticated user: '{request.user.email}'")
        return super().get(request, *args, **kwargs)
