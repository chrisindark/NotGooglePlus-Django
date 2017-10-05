import os
import boto3

from uuid import uuid4

from botocore.config import Config
from django.conf import settings

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete


TMP_DOWNLOAD_PATH = 'tmp/'
CONTENT_UPLOAD_PATH = 'content/'
THUMBNAIL_UPLOAD_PATH = 'thumbnail/'
CONTENT_PREVIEW_UPLOAD_PATH = 'content_preview/'

content_file_path = '{0}{1}'.format(
    CONTENT_UPLOAD_PATH,
    uuid4()
)
preview_file_path = '{0}{1}'.format(
    CONTENT_PREVIEW_UPLOAD_PATH,
    uuid4()
)


class AwsUtility(object):
    s3 = None

    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_HOST,
            region_name=settings.AWS_S3_DEFAULT_REGION,
            config=Config(signature_version='s3v4')
        )

        # Make sure everything posted is publicly readable
        # date_short = datetime.datetime.utcnow().strftime('%Y%m%d')
        # date_long = datetime.datetime.utcnow().strftime('%Y%m%dT000000Z')
        # self.fields = {
        #     "acl": "public-read"
        #     "acl": "private",
        #     "date": date_short,
        #     "region": settings.AWS_DEFAULT_REGION,
        #     "x-amz-algorithm": "AWS4-HMAC-SHA256",
        #     "x-amz-date": date_long
        # }

        # Ensure that the ACL isn't changed and restrict the user to a length
        # between 10 and 100.
        # self.conditions = [
        #     {"acl": "public-read"},
        #     ["content-length-range", 10, 100]
        # ]

        # self.config = Config(signature_version='s3v4')

    def create_s3_bucket(self, bucket_name=None):
        bucket_name = bucket_name or settings.AWS_STORAGE_BUCKET_NAME
        return self.s3.create_bucket(Bucket=bucket_name)

    def list_s3_buckets(self):
        return self.s3.buckets.all()

    def get_presigned_post(self, key, expires_in=60):
        presigned_post = self.s3.generate_presigned_post(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            ExpiresIn=expires_in
        )

        return presigned_post

    def get_multipart_upload(self, key, expires_in=60):
        multipart_upload = self.s3.create_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Expires=expires_in
        )

        return multipart_upload

    def get_presigned_put_url(self, key, expires_in=60):
        presigned_url = self.s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': key,
            },
            ExpiresIn=expires_in
        )

        return presigned_url

    def get_presigned_get_url(self, key, expires_in=60):
        presigned_url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': key,
            },
            ExpiresIn=expires_in
        )

        return presigned_url

    def get_object_metadata(self, key):
        object_metadata = self.s3.head_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
        )

        return object_metadata

    def get_uuid_from_key(self, key):
        return key.split('/')[1]

    def get_thumbnail_key(self, key):
        return 'thumbnail/' + self.get_uuid_from_key(key)

    def get_content_file_path(self, key):
        return os.path.join(
            settings.PROJECT_PATH,
            settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + key
        )

    def get_content_directory_path(self):
        return os.path.join(
            settings.PROJECT_PATH,
            settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + CONTENT_UPLOAD_PATH
        )

    def download_fileobj(self, key):
        # get tmp folder path and create if not existing
        tmp_content_directory_path = self.get_content_directory_path()
        if not os.path.exists(tmp_content_directory_path):
            os.makedirs(tmp_content_directory_path)

        tmp_content_file_path = self.get_content_file_path(key)
        # download the file object into the tmp folder with the key provided
        self.s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, key, tmp_content_file_path)

    def upload_fileobj(self, file_path, key):
        # upload the file object from the file_path to s3 using the key sent
        self.s3.upload_file(
            os.path.join(
                settings.PROJECT_PATH,
                settings.MEDIA_PATH + file_path
            ), settings.AWS_STORAGE_BUCKET_NAME, key)

    def create_thumbnail(self, key):
        # create a thumbnail for the file downloaded into the tmp folder
        # and return the thumbnail object
        return get_thumbnail(os.path.join(
            settings.PROJECT_PATH,
            settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + key),
            '100x50', crop='center', quality=99)

    def cleanup_server_files(self, s3_thumbnail, tmp_content_file_path):
        # remove the downloaded files from the server using
        delete(s3_thumbnail)
        delete(tmp_content_file_path)
