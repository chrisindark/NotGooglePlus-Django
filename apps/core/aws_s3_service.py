import logging
from uuid import uuid4

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.template.defaultfilters import slugify

from apps.core.constants import AWS_S3_FILE_NAME_MAX_LENGTH

# from sorl.thumbnail import get_thumbnail
# from sorl.thumbnail import delete

logger = logging.getLogger(__name__)

TMP_DOWNLOAD_PATH = "tmp/"
CONTENT_UPLOAD_PATH = "content/"
THUMBNAIL_UPLOAD_PATH = "thumbnail/"
CONTENT_PREVIEW_UPLOAD_PATH = "content_preview/"

content_file_path = f"{0}{1}".format(CONTENT_UPLOAD_PATH, uuid4())
preview_file_path = f"{0}{1}".format(CONTENT_PREVIEW_UPLOAD_PATH, uuid4())


class AwsS3Service:
    def __init__(
        self,
        access_key,
        secret_key,
        bucket_name,
        region,
        endpoint_url=None,
    ):

        self.bucket = bucket_name
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            endpoint_url=endpoint_url,
            config=Config(signature_version="s3v4"),
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
        try:
            bucket_name = bucket_name or self.bucket
            return self.client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logger.error(f"Create bucket failed: {e}")
            raise RuntimeError(f"Create bucket failed: {e}")

    def list_s3_buckets(self):
        try:
            return self.client.list_buckets()
        except ClientError as e:
            logger.error(f"List buckets failed: {e}")
            raise RuntimeError(f"List buckets failed: {e}")

    def normalize_and_truncate_file_name(self, file_name: str):
        [file_name, file_extension] = file_name.split(".")
        file_name = slugify(file_name)
        file_name = f"{file_name}.{file_extension}"[:AWS_S3_FILE_NAME_MAX_LENGTH]
        return file_name

    def generate_key(self, folder_name, file_name):
        uuid_str = uuid4()

        file_name = self.normalize_and_truncate_file_name(file_name)
        return f"{folder_name}_{uuid_str}_{file_name}"

    def get_presigned_post(self, key, expires_in=3600, content_type: str | None = None):
        try:
            fields = {}
            conditions = []

            if content_type:
                fields["ContentType"] = content_type
                conditions.append({"ContentType": content_type})

            return self.client.generate_presigned_post(
                Bucket=self.bucket,
                Key=key,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(f"Presigned Post URL generation failed: {e}")
            raise RuntimeError(f"Presigned Post URL generation failed: {e}")

    def get_presigned_put_url(
        self, key, expires_in=3600, content_type: str | None = None
    ):
        try:
            params = {"Bucket": self.bucket, "Key": key}
            if content_type:
                params["ContentType"] = content_type

            return self.client.generate_presigned_url(
                ClientMethod="put_object",
                Params=params,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(f"Presigned Put URL generation failed: {e}")
            raise RuntimeError(f"Presigned Put URL generation failed: {e}")

    def get_presigned_get_url(self, key, expires_in=3600):
        try:
            params = {"Bucket": self.bucket, "Key": key}
            return self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params=params,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(f"Presigned Get URL generation failed: {e}")
            raise RuntimeError(f"Presigned Get URL generation failed: {e}")

    def get_object_metadata(self, key):
        try:
            return self.client.head_object(
                Bucket=self.bucket,
                Key=key,
            )

        except ClientError as e:
            logger.error(f"Metadata Get failed: {e}")
            raise RuntimeError(f"Metadata Get failed: {e}")

    def create_multipart_upload(self, key):
        try:
            return self.client.create_multipart_upload(Bucket=self.bucket, Key=key)
        except ClientError as e:
            logger.error(f"Create multipart upload failed: {e}")
            raise RuntimeError(f"Create multipart upload failed: {e}")

    def upload_part(
        self,
        key: str,
        upload_id: str,
        part_number: int,
        body: bytes,
    ):
        try:
            return self.client.upload_part(
                Bucket=self.bucket,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=body,
            )
        except ClientError as e:
            logger.error(f"Upload part failed: {e}")
            raise RuntimeError(f"Upload part failed: {e}")

    def complete_multipart_upload(
        self,
        key: str,
        upload_id: str,
        parts: list,
    ):
        try:
            return self.client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )
        except ClientError as e:
            logger.error(f"Multipart completion failed: {e}")
            raise RuntimeError(f"Multipart completion failed: {e}")

    def abort_multipart_upload(self, key: str, upload_id: str) -> None:
        try:
            self.client.abort_multipart_upload(
                Bucket=self.bucket,
                Key=key,
                UploadId=upload_id,
            )
        except ClientError as e:
            logger.error(f"Abort multipart failed: {e}")
            raise RuntimeError(f"Abort multipart failed: {e}")

    # def get_uuid_from_key(self, key):
    #     return key.split('/')[1]

    # def get_thumbnail_key(self, key):
    #     return 'thumbnail/' + self.get_uuid_from_key(key)

    # def get_content_file_path(self, key):
    #     return os.path.join(
    #         settings.PROJECT_PATH,
    #         settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + key
    #     )

    # def get_content_directory_path(self):
    #     return os.path.join(
    #         settings.PROJECT_PATH,
    #         settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + CONTENT_UPLOAD_PATH
    #     )

    # def download_fileobj(self, key):
    #     # get tmp folder path and create if not existing
    #     tmp_content_directory_path = self.get_content_directory_path()
    #     if not os.path.exists(tmp_content_directory_path):
    #         os.makedirs(tmp_content_directory_path)

    #     tmp_content_file_path = self.get_content_file_path(key)
    #     # download the file object into the tmp folder with the key provided
    #     self.client.download_file(self.bucket, key, tmp_content_file_path)

    # def upload_fileobj(self, file_path, key):
    #     # upload the file object from the file_path to s3 using the key sent
    #     self.client.upload_file(
    #         os.path.join(
    #             settings.PROJECT_PATH,
    #             settings.MEDIA_PATH + file_path
    #         ), self.bucket, key)

    # def create_thumbnail(self, key):
    #     # create a thumbnail for the file downloaded into the tmp folder
    #     # and return the thumbnail object
    #     return get_thumbnail(os.path.join(
    #         settings.PROJECT_PATH,
    #         settings.MEDIA_PATH + TMP_DOWNLOAD_PATH + key),
    #         '100x50', crop='center', quality=99)

    # def cleanup_server_files(self, s3_thumbnail, tmp_content_file_path):
    #     # remove the downloaded files from the server using
    #     delete(s3_thumbnail)
    #     delete(tmp_content_file_path)
