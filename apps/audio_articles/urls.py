from django.urls import include, path
from rest_framework import routers

from apps.audio_articles.views import AudioArticleViewSet, TestArticleToAudioView

router = routers.SimpleRouter()
router.register("", AudioArticleViewSet)

urlpatterns = [path("", include(router.urls))]

urlpatterns += [
    path('test/synthesize', TestArticleToAudioView.as_view(), name='test-article-to-audio'),
]
