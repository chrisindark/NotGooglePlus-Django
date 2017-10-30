from apps.core.views import *
from rest_framework import viewsets, generics, pagination

from apps.accounts.permissions import *
from .filters import *
from .serializers import *


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
        queryset = self.get_serializer_class().annotate_likes_dislikes_count(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ArticleIdListView(ModelIdListMixin):
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    filter_class = ArticleFilter


class ArticleLikeMixin(generics.GenericAPIView):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer

    def get_queryset(self):
        queryset = super(ArticleLikeMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(article__id=self.kwargs.get('article__id'))


class ArticleLikeListCreateView(ArticleLikeMixin, generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.kwargs.get('article__id'))
        serializer.save(user=self.request.user.profile, article=article)


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

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.kwargs.get('article__id'))
        serializer.save(user=self.request.user.profile, article=article)


class ArticleCommentListCreateView(ArticleCommentMixin, generics.ListCreateAPIView):
    pass
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(),)


class ArticleCommentDetailView(ArticleCommentMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(), IsOwner(),)


class ArticleCommentLikeListCreateView(generics.ListCreateAPIView):
    queryset = ArticleCommentLike.objects.all()
    serializer_class = ArticleCommentLikeSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(
            article_comment__article__id=self.kwargs.get('article__id'),
            article_comment__id=self.kwargs.get('pk')
        )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        article_comment = ArticleComment.objects.get(id=self.kwargs.get('pk'))
        serializer.save(user=self.request.user.profile, article_comment=article_comment)
