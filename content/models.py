from uuid import uuid4

from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models

from notgoogleplus.apps.core.models import TimestampedModel
from notgoogleplus.apps.core.awsutility import AwsUtility

from .constants import *


content_file_path = '{0}{1}'.format(
    CONTENT_UPLOAD_PATH,
    uuid4()
)
preview_file_path = '{0}{1}'.format(
    CONTENT_PREVIEW_UPLOAD_PATH,
    uuid4()
)


# Create your models here.
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
    file_size = models.IntegerField(
        verbose_name=_('File size'),
        help_text=_('Size of the file in bytes')
    )
    file_type = models.IntegerField(
        choices=S3_UPLOAD_FILE_TYPE_CHOICES,
        verbose_name=_('Preview file or Content file')
    )
    key = models.CharField(
        max_length=255,
        verbose_name=_('Key'),
        help_text=_('Key of the file being uploaded')
    )
    last_modified = models.BigIntegerField(
        verbose_name=_('Last Modified'),
        help_text=_('Last Modified Date in seconds')
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
        return '<S3MultipartUpload: {}>'.format(self.file_name)


class Content(TimestampedModel):
    """The class is used for storing content information."""

    user = models.ForeignKey(
        'profiles.Profile',
        verbose_name=_('Profile'),
        related_name='profile_content_downloads'
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Content name'),
        help_text=_('Title used as text for this content type')
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text='Unique content URL, created from title.',
        verbose_name='Url for the content'
    )
    description = models.TextField(
        default="",
        null=True,
        blank=True,
        help_text=_("Text to describe the content")
    )
    s3_file = models.OneToOneField(
        S3FileUpload,
        verbose_name='Uploaded Content',
        help_text=_('uploaded_content')
    )
    content_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_("Content Cost"),
        help_text=_("Price for the content"),
    )
    # content_file_type = models.IntegerField(
    #     choices=S3_UPLOAD_FILE_TYPE_CHOICES,
    #     verbose_name=_('Preview file or Content file')
    # )
    # content_type = models.IntegerField(
    #     choices=CONTENT_TYPE_CHOICES,
    #     verbose_name=_("Type of content being uploaded")
    # )
    # content_duration = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     choices=VIDEO_LENGTH_CHOICES,
    #     verbose_name=_("File duration in case of audio or video")
    # )
    # uploaded_on = models.DateTimeField(
    #     auto_now_add=True
    # )
    number_of_downloads = models.IntegerField(
        default=0,
        verbose_name=_("Number of times this content got downloaded")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Active content is only shown to the user")
    )
    average_rating = models.IntegerField(
        default=0,
        verbose_name=_("Current average rating of the content")
    )
    # content_file = models.FileField(
    #     verbose_name=_('Content File'),
    #     upload_to=CONTENT_UPLOAD_PATH,
    #     null=True
    # )
    # preview_file = models.FileField(
    #     verbose_name=_('Preview File'),
    #     upload_to=CONTENT_PREVIEW_UPLOAD_PATH,
    #     null=True
    # )
    # thumbnail = models.ImageField(
    #     verbose_name=_('Thumbnail Image'),
    #     upload_to=CONTENT_THUMBNAIL_UPLOAD_PATH,
    # )
    # thumbnails = models.CharField(
    #     verbose_name=_('Content File thumbnail data'),
    #     blank=True,
    #     null=True
    # )

    # def populate_thumbnail(self):
    #     if self.thumbnails is None:
    #         self.thumbnails = {}
    #
    #     thumbnails_to_populate = list(
    #         set(THUMBNAIL_SIZES) - set(self.thumbnails)
    #     )
    #
    #    for thumbnail in thumbnails_to_populate:
    #        from sorl.thumbnail import get_thumbnail
    #        im = get_thumbnail(
    #             self.thumbnail,
    #             THUMBNAIL_SIZES[thumbnail],
    #             crop='center',
    #             quality=99
    #         )
    #         self.thumbnails[thumbnail] = im.url[:im.url.find('?')]
    #         self.save()
    #
    def __str__(self):
        return self.s3_file
    
    def __repr__(self):
        return '<Content: {}>'.format(self.s3_file)
    
    # def get_preview_download_link(self):
    #     if not self.preview_file:
    #         return None
    #
    #     # move to a utils file in case it needs to be used elsewhere too
    #     try:
    #         aws_utility = AwsUtility()
    #
    #         fetch_url = aws_utility.s3.generate_presigned_url(
    #             expires_in=600,  # valid for 600 seconds
    #             method='GET',
    #             key=self.preview_file.name,
    #             bucket=settings.AWS_STORAGE_BUCKET_NAME,
    #             response_headers={
    #                 'response-content-type': 'application/octet-stream'
    #             })
    #         return fetch_url
    #     except Exception as e:
    #         return e
    
    # def get_content_download_link(self):
    #     try:
    #         aws_utility = AwsUtility()
    #         fetch_url = aws_utility.s3.generate_presigned_url(
    #             expires_in=600,  # valid for 60 seconds
    #             method='GET',
    #             key=self.content_file.name,
    #             bucket=settings.AWS_STORAGE_BUCKET_NAME,
    #             response_headers={
    #                 'response-content-type': 'application/octet-stream'
    #             })
    #         return fetch_url
    #     except Exception as e:
    #         return e
