from django.conf import settings
from rest_framework import permissions

from apps.common.constants import INTERNAL_SERVICE_KEY_HEADER


class IsInternalService(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        return (
            request.headers.get(INTERNAL_SERVICE_KEY_HEADER)
            == settings.INTERNAL_SERVICE_KEY
        )
