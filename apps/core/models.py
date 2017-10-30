from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models


# Create your models here.
class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = [
            '-created_at',
            # '-updated_at'
        ]


# Create a ReadOnlySerializer to fetch the application details
# if needed on the frontend. Add a single object to the model
# and update the object directly in a management command
class AppModel(TimestampedModel):
    # A field to save application version according to semantic versioning
    # Given a version number MAJOR.MINOR.PATCH, increment the:
    # MAJOR version when you make incompatible API changes,
    # MINOR version when you add functionality in a backwards-compatible manner, and
    # PATCH version when you make backwards-compatible bug fixes.
    app_version = models.CharField(max_length=8, default='1.0.0')
    api_root = models.CharField(max_length=255, default='', blank=True)
    static_root = models.CharField(max_length=255, default='', blank=True)
    media_root = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.app_version

    def __repr__(self):
        return '<AppModel: {app_version}>'.format(app_version=self.app_version)


class S3FileUpload(TimestampedModel):
    """
    This class stores the data of S3 multipart upload to track the upload

    It stores the file key, upload id, file details and the chunks uploaded
    to S3 server.
    """

    file_name = models.CharField(
        max_length=255,
        verbose_name=_('File name '),
        help_text=_('Name of the file with which user uploaded')
    )
    file_size = models.BigIntegerField(
        verbose_name=_('File size'),
        help_text=_('Size of the file in bytes')
    )
    file_type = models.CharField(
        max_length=5,
        verbose_name=_('File type'),
        help_text=_('Type of file content')
    )
    file_content_type = models.CharField(
        max_length=20,
        verbose_name=_('File content type'),
        help_text=_('Content type of file')
    )
    key = models.CharField(
        max_length=255,
        verbose_name=_('Key'),
        help_text=_('Key of the file being uploaded')
    )
    last_modified = models.DateTimeField(
        verbose_name=_('Last Modified'),
        help_text=_('Last Modified Date')
    )
    # upload_id = models.CharField(
    #     max_length=255,
    #     verbose_name=_('Upload ID'),
    #     help_text=_('Upload Id to identify each upload uniquely')
    # )
    # chunks_uploaded = models.TextField(
    #     default='',
    #     verbose_name=_('Chunks Uploaded'),
    #     help_text=_('List of chunks that are uploaded to S3 server')
    # )

    def __str__(self):
        return self.file_name

    def __repr__(self):
        return '<S3FileUpload: {}>'.format(self.file_name)
