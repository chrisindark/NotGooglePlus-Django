from django.urls import include, path
from rest_framework import routers

from .views import PostIdListView, PostViewSet

router = routers.SimpleRouter()
router.register("", PostViewSet)

urlpatterns = (
    path("ids/", PostIdListView.as_view(), name="post-id-list"),
    path("", include(router.urls)),
    # path(
    #     r"posts/(?P<post__id>[^/.]+)/comments/$",
    #     PostCommentListCreateView.as_view(),
    #     name="post-comment-list",
    # ),
    # path(
    #     r"posts/(?P<post__id>[^/.]+)/comments/(?P<pk>[^/.]+)/$",
    #     PostCommentDetailView.as_view(),
    #     name="post-comment-detail",
    # ),
    # path(
    #     r"posts/(?P<post__id>[^/.]+)/likes/$",
    #     PostLikeListCreateView.as_view(),
    #     name="post-like-list",
    # ),
    # path(
    #     r"posts/(?P<post__id>[^/.]+)/comments/(?P<pk>[^/.]+)/likes/$",
    #     PostCommentLikeListCreateView.as_view(),
    #     name="post-comment-like-list",
    # ),
)
