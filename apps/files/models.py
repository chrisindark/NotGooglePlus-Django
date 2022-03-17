from django.db import models
from django.conf import settings

from apps.core.models import TimestampedModel


# Create your models here.
def file_path_fn(instance, filename):
    # file_path = settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.user_id, instance.file_name)
    file_path = settings.FILE_UPLOAD_PATH + \
        '{0}/{1}'.format(instance.file_name, instance.file_name)
    return file_path


def file_directory_path_fn(instance):
    # file_directory_path = settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + '{0}'.format(instance.user_id)
    file_directory_path = settings.MEDIA_PATH + \
        settings.FILE_UPLOAD_PATH + '{0}'.format(instance.file_name)
    return file_directory_path


def thumbnail_file_directory_fn(instance):
    thumbnail_file_directory_path = settings.MEDIA_PATH + \
        settings.FILE_THUMBNAIL_PATH + '{0}'.format(instance.file_name)
    return thumbnail_file_directory_path


class FileUpload(TimestampedModel):
    user = models.ForeignKey(
        'profiles.Profile', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=file_path_fn, max_length=255
    )
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=5)
    file_content_type = models.CharField(max_length=20)
    file_size = models.BigIntegerField(default=0)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name + self.file_content_type

    def __repr__(self):
        return '<FileUpload: {file_name}>'.format(file_name=self.file_name)


# class S3FileUpload(TimestampedModel):
#     """
#     This class stores the data of S3 multipart upload to track the upload

#     It stores the file key, upload id, file details and the chunks uploaded
#     to S3 server.
#     """

#     file_name = models.CharField(
#         max_length=255,
#         verbose_name=_('File name '),
#         help_text=_('Name of the file with which user uploaded')
#     )
#     file_size = models.BigIntegerField(
#         verbose_name=_('File size'),
#         help_text=_('Size of the file in bytes')
#     )
#     file_type = models.CharField(
#         max_length=5,
#         verbose_name=_('File type'),
#         help_text=_('Type of file content')
#     )
#     file_content_type = models.CharField(
#         max_length=20,
#         verbose_name=_('File content type'),
#         help_text=_('Content type of file')
#     )
#     key = models.CharField(
#         max_length=255,
#         verbose_name=_('Key'),
#         help_text=_('Key of the file being uploaded')
#     )
#     last_modified = models.DateTimeField(
#         verbose_name=_('Last Modified'),
#         help_text=_('Last Modified Date')
#     )
#     # upload_id = models.CharField(
#     #     max_length=255,
#     #     verbose_name=_('Upload ID'),
#     #     help_text=_('Upload Id to identify each upload uniquely')
#     # )
#     # chunks_uploaded = models.TextField(
#     #     default='',
#     #     verbose_name=_('Chunks Uploaded'),
#     #     help_text=_('List of chunks that are uploaded to S3 server')
#     # )

#     def __str__(self):
#         return self.file_name

#     def __repr__(self):
#         return '<S3FileUpload: {}>'.format(self.file_name)
