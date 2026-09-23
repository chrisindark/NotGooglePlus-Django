from django.shortcuts import get_object_or_404
from rest_framework import permissions

from apps.profiles.models import Profile


class IsAudioArticleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = request.user
            profile = get_object_or_404(Profile, user=user)
            return profile == obj.profile
        return False
