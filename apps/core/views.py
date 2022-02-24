from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    S3FileUpload
)
from .serializers import (
    ModelIdSerializer, S3CreateFileSignatureSerializer,
    S3FileUploadSerializer, S3FileSignedSerializer,
    S3UpdateFileSignatureSerializer
)


# Create your views here.
class ModelIdListMixin(generics.ListAPIView):
    serializer_class = ModelIdSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

    def get_queryset(self):
        queryset = self.queryset.values_list('id', flat=True)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = [key['id'] for key in serializer.data]
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = [key['id'] for key in serializer.data]

        return Response(data)


class CreateListMixin(object):
    """Allows bulk creation of a resource."""

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)


# class S3FileSignatureView(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = S3CreateFileSignatureSerializer

#     """
#     Provides the S3 file upload url
#     """
#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, *args, **kwargs):
#         serializer = S3UpdateFileSignatureSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class S3FileUploadListView(generics.ListAPIView):
#     queryset = S3FileUpload.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = S3FileUploadSerializer
#     """
#         Sends list of s3 files saved in database
#     """


# class S3FileUploadCreateView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = S3FileUploadSerializer

#     """
#     Sends list of s3 files saved in database
#     Saves s3 file data to database
#     """

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class S3FileSignedView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = S3FileSignedSerializer

#     """
#     Provides the S3 file url for viewing
#     """

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
