import logging

from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.core.aws_s3_service import AwsS3Service
from apps.core.models import AppConfig
from apps.core.serializers import AppConfigSerializer, CreateSignedUrlSerializer

logger = logging.getLogger(__name__)


# Create your views here.
class AppConfigRetrieveDetailView(generics.RetrieveAPIView):
    serializer_class = AppConfigSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return AppConfig.get_solo()


class AppConfigUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AppConfigSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        return AppConfig.get_solo()


class CreateSignedUrlView(generics.RetrieveUpdateAPIView):
    """
    Provides the S3 file upload url
    """

    serializer_class = CreateSignedUrlSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.create_aws_s3_presigned_url(serializer)
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.create_aws_s3_presigned_url(serializer)
        return Response(response, status=status.HTTP_200_OK)

    def create_aws_client(self):
        access_key = settings.AWS_ACCESS_KEY_ID
        secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        region = settings.AWS_S3_DEFAULT_REGION
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        aws_s3_client = AwsS3Service(
            access_key, secret_access_key, bucket_name, region, endpoint_url
        )
        return aws_s3_client

    def create_aws_s3_presigned_url(self, serializer):
        folder_name = serializer.validated_data.get("folder_name")
        file_name = serializer.validated_data.get("file_name")
        content_type = serializer.validated_data.get("content_type")

        aws_s3_client = self.create_aws_client()
        key = aws_s3_client.generate_key(folder_name, file_name)
        logger.debug(f"presigned url key: {key}")
        presigned_put_url = aws_s3_client.get_presigned_put_url(
            key=key, expires_in=60, content_type=content_type
        )
        logger.debug(f"presigned put url: {presigned_put_url}")
        return {"key": key, "upload_url": presigned_put_url}
