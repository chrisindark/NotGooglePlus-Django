import django_filters

from .models import *


class ArticleFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name="user__user__username")
    o = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Article
        fields = (
            'created_at',
        )


class ArticleCommentFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = ArticleComment
        fields = (
            'article__id',
            'created_at',
        )
