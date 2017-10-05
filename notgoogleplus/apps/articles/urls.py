from django.conf.urls import include, url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ArticleViewSet, TagViewSet,
    ArticleIdListView,
    ArticleCommentListCreateView,
    ArticleCommentDetailView,
    ArticleLikeListCreateView,
    ArticleCommentLikeListCreateView,
)
from .search_indexes import ArticleIndexViewSet


router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)


router.register(r'search_articles', ArticleIndexViewSet, base_name='search_articles')

urlpatterns = (
    url(r'articles/ids/$', ArticleIdListView.as_view(), name='article-id-list'),
    url(r'articles/(?P<article__id>[^/.]+)/comments/$',
        ArticleCommentListCreateView.as_view(), name='article-comment-list'),
    url(r'articles/(?P<article__id>[^/.]+)/comments/(?P<pk>[^/.]+)/$',
        ArticleCommentDetailView.as_view(), name='article-comment-detail'),
    url(r'articles/(?P<article__id>[^/.]+)/likes/$',
        ArticleLikeListCreateView.as_view(), name='article-like-list'),
    url(r'articles/(?P<article__id>[^/.]+)/comments/(?P<pk>[^/.]+)/likes/$',
        ArticleCommentLikeListCreateView.as_view(), name='article-comment-like-list'),

    url(r'', include(router.urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)
