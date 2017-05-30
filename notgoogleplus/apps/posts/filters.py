import django_filters

from .models import *


class PostFilter(django_filters.FilterSet):
    # user_id = django_filters.CharFilter(name="user__id")
    # user_email = django_filters.CharFilter(name="user__user__email")
    username = django_filters.CharFilter(name="user__user__username")
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Post
        fields = (
            'created_at',
        )


class PostCommentFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = PostComment
        fields = (
            'created_at',
        )


class FileFilter(django_filters.FilterSet):
    class Meta(PostFilter.Meta):
        model = File
