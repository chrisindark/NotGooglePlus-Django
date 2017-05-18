import django_filters

from .models import *


class ArticleFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Article
        fields = (
            'user__user__username',
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
