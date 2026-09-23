from django.urls import include, path
from rest_framework import routers

from apps.audio_posts.views import AudioPostViewSet, TestPostToAudioView

router = routers.SimpleRouter()
router.register("", AudioPostViewSet)

urlpatterns = [path("", include(router.urls))]

urlpatterns += [
    path('test/synthesize', TestPostToAudioView.as_view(), name='test-post-to-audio'),
]
