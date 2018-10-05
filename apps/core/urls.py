from django.conf.urls import include, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    S3FileSignatureView, S3FileUploadListView,
    S3FileUploadCreateView, S3FileSignedView
)


urlpatterns = (
    url(r's3/files/signature/$', S3FileSignatureView.as_view(), name='s3-files-signature'),
    url(r's3/files/$', S3FileUploadListView.as_view(), name='s3-files'),
    url(r's3/files/upload/finished/$', S3FileUploadCreateView.as_view(), name='s3-files-upload-finished'),
    url(r's3/files/signed/$', S3FileSignedView.as_view(), name='s3-files-signed'),

    # url(r'content/(?P<slug>[\-\d\w]+)/$', ContentDetailView.as_view(), name='content_detail'),
    # url(r'^my_contents/$', ContentDownloadListView.as_view(), name='my_content_list'),
    # url(r'^my_content/(?P<pk>[\-\d\w]+)/$', ContentDownloadDetailView.as_view(), name='my_content_list'),
    # url(r'content/(?P<id>\d+)/pay/$', ContentPayAndDownloadView.as_view(), name='pay_for_content'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
