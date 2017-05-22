from rest_framework import permissions, viewsets, generics, pagination

from notgoogleplus.apps.accounts.permissions import *

from .models import *
from .serializers import *
from .filters import *


# Create your views here.
class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.

    retrieve:
    Return a post instance.

    list:
    Return paginated posts, ordered by most recently added.

    update:
    Update content of a post instance

    delete:
    Delete a post instance
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_class = PostFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        # Set up eager loading to avoid N+1 selects
        queryset = self.get_serializer_class().setup_eager_loading(self.queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class PostCommentPagination(PostPagination):
    pass


# class PostCommentViewSet(viewsets.ModelViewSet):
#     queryset = PostComment.objects.all()
#     serializer_class = PostCommentSerializer
#     pagination_class = PostCommentPagination
#     filter_class = PostCommentFilter

#     def get_permissions(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return (permissions.AllowAny(),)
#         return (permissions.IsAuthenticated(), IsCommentOwner(),)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class PostCommentMixin(generics.GenericAPIView):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    pagination_class = PostCommentPagination

    def get_queryset(self):
        queryset = super(PostCommentMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        if self.kwargs.get('pk'):
            return queryset.filter(pk=self.kwargs.get('pk'))
        return queryset.filter(post__id=self.kwargs.get('post__id'))


class PostCommentListCreateView(PostCommentMixin, generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post__id'))
        serializer.save(user=self.request.user, post=post)


class PostCommentDetailView(PostCommentMixin, generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        return (permissions.IsAuthenticated(), IsOwner(),)


class FilePagination(PostPagination):
    pass


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pagination_class = FilePagination
    filter_class = FileFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
