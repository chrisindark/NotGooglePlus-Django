from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj.user.user == request.user
        return False


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if request.user and request.user.is_authenticated():
            return False
        return True
