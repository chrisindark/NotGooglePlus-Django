from django.urls import include, path
from rest_framework import routers

from apps.tags.views import TagViewSet

router = routers.SimpleRouter()
router.register("", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
