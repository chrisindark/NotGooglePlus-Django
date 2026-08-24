import binascii
import os

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import mixins, permissions, viewsets

from apps.profiles.models import Profile
from apps.tags.constants import TAG_SLUG_MAX_LENGTH
from apps.tags.models import Tag
from apps.tags.pagination import TagPagination
from apps.tags.serializers import TagSerializer


# Create your views here.
class TagViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    A simple ViewSet for viewing tags.
    """

    queryset = Tag.objects.all().order_by("-created_at")
    serializer_class = TagSerializer
    pagination_class = TagPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        print("perform_create", serializer.validated_data)
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(created_by=profile)
        self.create_slug(serializer.instance)

    def perform_update(self, serializer):
        print("perform_update", serializer.validated_data)
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(updated_by=profile)
        self.create_slug(serializer.instance)

    def create_slug(self, tag):
        if tag.slug is not None and tag.slug != "":
            return tag

        slug = slugify(tag.tag)
        unique = binascii.hexlify(os.urandom(20)).decode()
        if len(slug) > TAG_SLUG_MAX_LENGTH:
            slug = slug[:TAG_SLUG_MAX_LENGTH]
        while len(slug + "-" + unique) > TAG_SLUG_MAX_LENGTH:
            parts = slug.split("-")
            if len(parts) == 1:
                slug = slug[:TAG_SLUG_MAX_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        final_slug = slug + "-" + unique
        tag.slug = final_slug
        tag.save()
        return tag
