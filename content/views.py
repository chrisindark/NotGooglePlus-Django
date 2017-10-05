from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    S3FileUpload
)
from .serializers import (
    S3FileSignatureSerializer, S3FileUploadSerializer, S3FileSignedSerializer,
)


# Create your views here.
class S3FileSignatureView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = S3FileSignatureSerializer

    """
    Provides the S3 file upload url
    """
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class S3FileUploadListView(generics.ListAPIView):
    queryset = S3FileUpload.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = S3FileUploadSerializer
    """
        Sends list of s3 files saved in database
    """


class S3FileUploadCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = S3FileUploadSerializer

    """
    Sends list of s3 files saved in database
    Saves s3 file data to database
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class S3FileSignedView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = S3FileSignedSerializer

    """
    Provides the S3 file url for viewing
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
