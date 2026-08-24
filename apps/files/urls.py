from django.urls import include, path
from rest_framework import routers

from .views import FileUploadViewSet

router = routers.SimpleRouter()
router.register("files/(?P<username>[^/.]+)", FileUploadViewSet)
router.register("files", FileUploadViewSet)

urlpatterns = (path("", include(router.urls)),)
