from django.db import models
from django.conf import settings

from apps.core.models import TimestampedModel


# Create your models here.
def file_path_fn(instance, filename):
    # file_path = settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.user_id, instance.file_name)
    file_path = settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.file_name, instance.file_name)
    return file_path


def file_directory_path_fn(instance):
    # file_directory_path = settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + '{0}'.format(instance.user_id)
    file_directory_path = settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + '{0}'.format(instance.file_name)
    return file_directory_path


def thumbnail_file_directory_fn(instance):
    thumbnail_file_directory_path = settings.MEDIA_PATH + settings.FILE_THUMBNAIL_PATH + '{0}'.format(instance.file_name)
    return thumbnail_file_directory_path


class FileUpload(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='files', on_delete=models.CASCADE)
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
