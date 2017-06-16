from rest_framework import permissions, viewsets, generics, mixins, pagination
from rest_framework.decorators import list_route

from notgoogleplus.apps.accounts.permissions import *

from .models import *
from .serializers import *
from .filters import *


# Create your views here.
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class ArticlePagination(pagination.PageNumberPagination):
    # page_size = 20
    page_size_query_param = 'page_size'
    # max_page_size = 1000


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_class = ArticleFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        # Set up eager loading to avoid N + 1 selects
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        queryset = self.get_serializer_class().annotate_comments_count(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ArticleIdListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_class = ArticleFilter

    # def get_permissions(self):
        # if self.request.method in permissions.SAFE_METHODS:
            # return (permissions.AllowAny(),)
        # pass

    def get_queryset(self):
        queryset = self.queryset.values_list('id', flat=True)

        return queryset


class ArticleCommentPagination(ArticlePagination):
    pass


class ArticleCommentMixin(generics.GenericAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    pagination_class = ArticleCommentPagination
    filter_class = ArticleCommentFilter

    def get_queryset(self):
        queryset = super(ArticleCommentMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(article__id=self.kwargs.get('article__id'))


class ArticleCommentListCreateView(ArticleCommentMixin, generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.kwargs.get('article__id'))
        serializer.save(user=self.request.user.profile, article=article)


class ArticleCommentDetailView(ArticleCommentMixin, generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)
