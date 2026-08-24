from django.urls import include, path
from rest_framework import routers

from .views import ArticleIdListView, ArticleViewSet

# from .search_indexes import ArticleIndexViewSet


router = routers.SimpleRouter()
router.register("", ArticleViewSet)


# router.register('search_articles', ArticleIndexViewSet, base_name='search_articles')

urlpatterns = [
    path("articles/ids/", ArticleIdListView.as_view(), name="article-id-list"),
    # path('articles/(?P<article__id>[^/.]+)/comments/',
    #     ArticleCommentListCreateView.as_view(), name='article-comment-list'),
    # path('articles/(?P<article__id>[^/.]+)/comments/(?P<pk>[^/.]+)/',
    #     ArticleCommentDetailView.as_view(), name='article-comment-detail'),
    # path('articles/(?P<article__id>[^/.]+)/likes/',
    #     ArticleLikeListCreateView.as_view(), name='article-like-list'),
    # path('articles/(?P<article__id>[^/.]+)/comments/(?P<pk>[^/.]+)/likes/',
    #     ArticleCommentLikeListCreateView.as_view(), name='article-comment-like-list'),
    path("", include(router.urls)),
]
