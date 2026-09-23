# from uuid import uuid4

# from django.db import models

# from apps.common.models import TimestampedModel

# from .constants import (
#     CONTENT_PREVIEW_UPLOAD_PATH,
#     CONTENT_UPLOAD_PATH,
#     S3_UPLOAD_FILE_TYPE_CHOICES,
# )

# content_file_path = f"{CONTENT_UPLOAD_PATH}{uuid4()}"
# preview_file_path = f"{CONTENT_PREVIEW_UPLOAD_PATH}{uuid4()}"


# # Create your models here.
# class S3FileUpload(TimestampedModel):
#     """
#     This class stores the data of S3 multipart upload to track the upload

#     It stores the file key, upload id, file details and the chunks uploaded
#     to S3 server.
#     """

#     file_name = models.CharField(
#         max_length=255,
#     )
#     file_size = models.BigIntegerField()
#     file_type = models.IntegerField(
#         choices=S3_UPLOAD_FILE_TYPE_CHOICES,
#     )
#     file_content_type = models.CharField(
#         max_length=20,
#     )
#     key = models.CharField(
#         max_length=255,
#     )
#     last_modified_at = models.DateTimeField()
#     uploaded_by = models.ForeignKey(
#         "profiles.Profile", related_name="s3_file_uploads", on_delete=models.DO_NOTHING
#     )
#     upload_id = models.CharField(
#         max_length=255,
#     )
#     chunks_uploaded = models.JSONField(
#         default="",
#     )

#     def __str__(self):
#         return self.file_name

#     def __repr__(self):
#         return f"<S3MultipartUpload: {self.file_name}>"


# class Content(TimestampedModel):
    # """The class is used for storing content information."""

    # profile = models.ForeignKey(
    #     "profiles.Profile",
    #     related_name="content_downloads",
    #     on_delete=models.DO_NOTHING,
    # )
    # title = models.CharField(
    #     max_length=255,
    #     null=True,
    #     blank=True,
    # )
    # slug = models.SlugField(
    #     max_length=50,
    #     unique=True,
    #     null=True,
    #     blank=True,
    # )
    # description = models.TextField(default="", null=True, blank=True)
    # s3_file = models.ForeignKey(
    #     "S3FileUpload",
    #     related_name="s3_file",
    #     on_delete=models.DO_NOTHING,
    # )
    # is_active = models.BooleanField(default=True)
    # content_price = models.DecimalField(
    #     max_digits=9,
    #     decimal_places=2,
    # )
    # content_file_type = models.IntegerField(
    #     choices=S3_UPLOAD_FILE_TYPE_CHOICES,
    # )
    # content_type = models.IntegerField(
    #     choices=CONTENT_TYPE_CHOICES,
    # )
    # content_duration = models.IntegerField(
    #     null=True,
    #     blank=True,
    #     choices=VIDEO_LENGTH_CHOICES,
    # )
    # uploaded_on = models.DateTimeField(
    #     auto_now_add=True
    # )
    # number_of_downloads = models.IntegerField(
    #     default=0
    # )
    # content_file = models.FileField(
    #     upload_to=CONTENT_UPLOAD_PATH,
    #     null=True
    # )
    # preview_file = models.FileField(
    #     upload_to=CONTENT_PREVIEW_UPLOAD_PATH,
    #     null=True
    # )
    # thumbnail = models.ImageField(
    #     upload_to=CONTENT_THUMBNAIL_UPLOAD_PATH,
    # )
    # thumbnails = models.CharField(
    #     blank=True,
    #     null=True
    # )
    # average_rating = models.IntegerField(default=0)

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
    # def __str__(self):
    #     return self.s3_file

    # def __repr__(self):
    #     return f"<Content: {self.s3_file}>"

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
