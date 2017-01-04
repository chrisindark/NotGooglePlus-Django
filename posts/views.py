from rest_framework import permissions, viewsets, status, generics
from rest_framework import pagination
from rest_framework.response import Response

from .models import *
from .permissions import *
from .serializers import *
from .filters import *

# Create your views here.
class PostPagination(pagination.PageNumberPagination):
     page_size = 10
     page_size_query_param = 'page_size'
     # max_page_size = 1000


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter
    pagination_class = PostPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        queryset = Post.objects.all()
        # Set up eager loading to avoid N+1 selects
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentPagination(pagination.PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     filter_class = CommentFilter
#     pagination_class = CommentPagination

#     def get_permissions(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return (permissions.AllowAny(),)
#         return (permissions.IsAuthenticated(), IsCommentOwner(),)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CommentMixin(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = super(CommentMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        if self.kwargs.get('pk'):
            return queryset.filter(pk=self.kwargs.get('pk'))
        return queryset.filter(post__id=self.kwargs.get('post__id'))


class CommentListCreateView(CommentMixin, generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post__id'))
        serializer.save(user=self.request.user, post=post)


class CommentDetailView(CommentMixin, generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        return (permissions.IsAuthenticated(), IsOwner(),)


class FileUploadPagination(pagination.PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    pagination_class = FileUploadPagination
    filter_class = FIleUploadFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
