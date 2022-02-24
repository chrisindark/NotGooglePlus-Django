import django_filters

from .models import *


class AccountFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(name="email", lookup_type="startswith")
    username = django_filters.CharFilter(
        name="username", lookup_type="startswith")

    class Meta:
        model = Account
        fields = (
            'email',
            'username',
        )
