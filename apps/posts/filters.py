import django_filters

from apps.core.filters import NumberInFilter
from .models import (
    Post, PostComment
)


class PostFilter(django_filters.FilterSet):
    # user_id = django_filters.CharFilter(name="user__id")
    # user_email = django_filters.CharFilter(name="user__user__email")
    ids = NumberInFilter(name='id', lookup_expr='in')
    username = django_filters.CharFilter(name='user__user__username')
    title__iexact = django_filters.CharFilter(name='title', lookup_expr='iexact')
    content__iexact = django_filters.CharFilter(name='content', lookup_expr='iexact')
    title__icontains = django_filters.CharFilter(name='title', lookup_expr='icontains')
    content__icontains = django_filters.CharFilter(name='content', lookup_expr='icontains')
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
