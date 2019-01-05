from django.conf.urls import url, include

from rest_framework import routers

from .views import FileUploadViewSet


router = routers.SimpleRouter()
# router.register(r'files/(?P<username>[^/.]+)', FileUploadViewSet)
router.register(r'files', FileUploadViewSet)

urlpatterns = (
    url(r'', include(router.urls)),
)
