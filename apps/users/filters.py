import django_filters

from .models import User


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(name="email", lookup_type="startswith")
    username = django_filters.CharFilter(name="username", lookup_type="startswith")

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )
