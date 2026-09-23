import logging
from uuid import uuid4

from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.aws_s3_service import AwsS3Service
from apps.core.models import AppConfig
from apps.core.serializers import (AppConfigSerializer,
                                   CreateSignedUrlSerializer)
from apps.core.tasks import add

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
        logger.info(f"presigned url key: {key}")
        presigned_put_url = aws_s3_client.get_presigned_put_url(
            key=key, expires_in=60, content_type=content_type
        )
        logger.info(f"presigned put url: {presigned_put_url}")
        return {"key": key, "upload_url": presigned_put_url}


class TestS3UploadView(APIView):
    """
    Generic test endpoint to upload a file directly to S3 through the Django backend.
    Takes 'folder_name' and 'file' in a multipart/form-data request.
    Returns the uploaded file's final S3 URL.
    """
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        upload_file = request.FILES.get("file")
        folder_name = request.data.get("folder_name", "test_uploads")

        if not upload_file:
            return Response(
                {"error": "No 'file' provided in form data."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate a safe key for S3
        ext = upload_file.name.split(".")[-1]
        key = f"{folder_name}/{uuid4()}.{ext}"

        try:
            # Initialize the custom AwsS3Service
            aws_s3_client = AwsS3Service(
                access_key=settings.AWS_ACCESS_KEY_ID,
                secret_key=settings.AWS_SECRET_ACCESS_KEY,
                bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                region=settings.AWS_S3_DEFAULT_REGION,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL
            )
            
            # Upload using the custom method
            file_url = aws_s3_client.upload_fileobj(upload_file, key)
            
            return Response({
                "message": "File successfully uploaded to S3.",
                "key": key,
                "file_url": file_url
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Test upload failed: {e}")
            return Response(
                {"error": "Failed to upload file to S3."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TestCeleryAddTaskView(APIView):
    """
    Test Celery task by adding two numbers.
    """
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        """
        Test Celery task by adding two numbers.
        """
        try:
            num1 = int(request.data.get("num1", 0))
            num2 = int(request.data.get("num2", 0))
            result = add.delay(num1, num2)
            logger.info(f"Celery task added successfully: {result.id}")
            logger.info(f"Celery task result: {result.get()}")
            return Response({
                "message": "Celery task added successfully.",
                "task_id": result.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Test Celery task failed: {e}")
            return Response(
                {"error": "Failed to add Celery task."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
