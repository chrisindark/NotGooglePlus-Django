from django.urls import path

from apps.core.views import (AppConfigRetrieveDetailView, AppConfigUpdateView,
                             CreateSignedUrlView, TestCeleryAddTaskView,
                             TestS3UploadView)

urlpatterns = (
    path(
        "app-config",
        AppConfigRetrieveDetailView().as_view(),
        name="app-config-retrieve-detail",
    ),
    path(
        "app-config/update",
        AppConfigUpdateView().as_view(),
        name="app-config-update",
    ),
    path("signed/url/create", CreateSignedUrlView.as_view(), name="signed-url-create"),
    path("test/upload", TestS3UploadView.as_view(), name="test-s3-upload"),
    path("test/celery/add", TestCeleryAddTaskView.as_view(), name="test-celery-add-task"),
    # path('s3/files/', S3FileUploadListView.as_view(), name='s3-files'),
    # path('s3/files/upload/finished/', S3FileUploadCreateView.as_view(), name='s3-files-upload-finished'),
    # path('s3/files/signed/', S3FileSignedView.as_view(), name='s3-files-signed'),
    # path('content/(?P<slug>[\-\d\w]+)/', ContentDetailView.as_view(), name='content_detail'),
    # path('^my_contents/', ContentDownloadListView.as_view(), name='my_content_list'),
    # path('^my_content/(?P<pk>[\-\d\w]+)/', ContentDownloadDetailView.as_view(), name='my_content_list'),
    # path('content/(?P<id>\d+)/pay/', ContentPayAndDownloadView.as_view(), name='pay_for_content'),
)
