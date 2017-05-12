import django_filters

from .models import *


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = (
            'user__username',
            'created_at',
        )
        order_by = (
            'created_at',
            '-created_at',
        )


class ArticleCommentFilter(django_filters.FilterSet):
    class Meta:
        model = ArticleComment
        fields = (
            'article__id',
            'created_at',
        )
        order_by = (
            'created_at',
            '-created_at',
        )
