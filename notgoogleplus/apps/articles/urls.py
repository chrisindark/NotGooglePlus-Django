from django.conf.urls import include, url

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = (
    url(r'^api/v1/', include(router.urls)),

    url(r'^api/v1/articles/(?P<article__id>[^/.]+)/comments/$',
        ArticleCommentListCreateView.as_view(), name='comment-list'),
    url(r'^api/v1/articles/(?P<article__id>[^/.]+)/comments/(?P<pk>[^/.]+)/$',
        ArticleCommentDetailView.as_view(), name='comment-detail'),
)
