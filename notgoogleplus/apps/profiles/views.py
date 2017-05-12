from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from notgoogleplus.apps.accounts.models import Account
from notgoogleplus.apps.accounts.permissions import *

from .models import Profile
from .serializers import ProfileSerializer, ProfileFollowSerializer


# Create your views here.
class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    lookup_field = 'user__username'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        try:
            kwargs = {'username': self.kwargs.get(self.lookup_field)}
            user = Account.objects.get(**kwargs)
            print(user)
            Profile.objects.get_or_create(user=user)
            queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
            return queryset
        except Account.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')


class ProfileFollowView(generics.UpdateAPIView):
    lookup_field = 'user__username'
    queryset = Profile.objects.all()
    serializer_class = ProfileFollowSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def get_queryset(self):
        queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
        return queryset
