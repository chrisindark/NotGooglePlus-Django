
from django.conf import settings
from rest_framework.exceptions import ValidationError
# from api.utility import webutil, ewoauthorization, appConstants
# from api.models.all import Employee
from uuid import uuid4
import boto3


class AwsUtility():

    upload_path = None

    def __init__(self, aws_path):
        self.upload_path = aws_path

    def getpresigneddata(self, id, request, file_name, file_type):
        if not file_name:
            raise ValidationError('No file name is provided')
        elif not file_type:
            raise ValidationError('No file type is provided.')

        s3_bucket = settings.S3_BUCKET
        ext = file_name.split('.')[-1]
        s3_path = self.upload_path.format(id, uuid4().hex, ext)

        s3 = boto3.client('s3', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        presigned_post = s3.generate_presigned_post(
            Bucket = s3_bucket,
            Key = s3_path,
            Fields = {"acl": "public-read", "Content-Type": file_type},
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn = 3600
        )

        return {
            'data': presigned_post,
            'url': 'https://{0}.s3.amazonaws.com/{1}'.format(s3_bucket, s3_path)
        }
