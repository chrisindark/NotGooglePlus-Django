import django_filters

from .models import *


class ProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name="user__username", lookup_expr="startswith")

    class Meta:
        model = Profile
        fields = {
            # 'user__username': ['startswith'],
        }
