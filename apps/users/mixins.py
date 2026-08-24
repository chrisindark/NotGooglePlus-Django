from rest_framework import generics

from apps.profiles.models import Profile
from apps.profiles.pagination import ProfilePagination
from apps.profiles.serializers import ProfileSerializer


class ProfileMixin(generics.GenericAPIView):
    queryset = Profile.objects.all().order_by("-created_at")
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
