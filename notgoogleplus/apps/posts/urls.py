from django.conf.urls import include, url

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'files', FileUploadViewSet)

urlpatterns = (
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/posts/(?P<post__id>[^/.]+)/comments/$', PostCommentListCreateView.as_view(), name='comment-list'),
    url(r'^api/v1/comments/(?P<pk>[^/.]+)/$', PostCommentDetailView.as_view(), name='comment-detail'),
)