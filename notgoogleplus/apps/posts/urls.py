from django.conf.urls import include, url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    PostViewSet,
    PostCommentListCreateView,
    PostCommentDetailView,
    PostIdListView,
    PostLikeListCreateView,
    PostCommentLikeListCreateView,
    FileUploadViewSet
)


router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'files/(?P<username>[^/.]+)', FileUploadViewSet)

urlpatterns = (
    url(r'posts/ids/$', PostIdListView.as_view(), name='post-id-list'),
    url(r'posts/(?P<post__id>[^/.]+)/comments/$',
        PostCommentListCreateView.as_view(), name='post-comment-list'),
    url(r'posts/(?P<post__id>[^/.]+)/comments/(?P<pk>[^/.]+)/$',
        PostCommentDetailView.as_view(), name='post-comment-detail'),
    url(r'posts/(?P<post__id>[^/.]+)/likes/$',
        PostLikeListCreateView.as_view(), name='post-like-list'),
    url(r'posts/(?P<post__id>[^/.]+)/comments/(?P<pk>[^/.]+)/likes/$',
        PostCommentLikeListCreateView.as_view(), name='post-comment-like-list'),

    url(r'', include(router.urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)
