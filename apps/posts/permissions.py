from rest_framework import permissions


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.profile == obj.profile
        return False
