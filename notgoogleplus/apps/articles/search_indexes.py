from haystack import indexes
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from rest_framework import serializers, permissions, viewsets, generics, mixins, pagination

from notgoogleplus.apps.accounts.permissions import *

from .models import Article
from .serializers import ArticleSerializer
from .views import ArticlePagination
from .filters import ArticleFilter


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='id')
    text = indexes.CharField(document=True, model_attr='content')
    description = indexes.CharField(model_attr='description')
    # user__user__username = indexes.CharField(model_attr='user__user__username')
    created_at = indexes.DateTimeField(model_attr='created_at')
    updated_at = indexes.DateTimeField(model_attr='updated_at')

    def get_model(self):
        return Article


class ArticleIndexSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    description = serializers.CharField()
    user__user__username = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        fields = ('id', 'text', 'description', 'created_at', 'updated_at', 'user__user__username')
        read_only_fields = ('id', 'text', 'description', 'created_at', 'updated_at', 'user__user__username')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ArticleIndexViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    model = Article
    serializer_class = ArticleIndexSerializer
    pagination_class = ArticlePagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet().models(self.model)

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            queryset = SearchQuerySet().models(self.model).filter(content=query)

        return queryset
