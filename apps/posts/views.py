from apps.core.views import ModelIdListMixin
from rest_framework import (
    permissions, viewsets, generics,
    pagination, parsers,
)

from apps.accounts.permissions import (
    IsOwner,
)
from .filters import (
    FileUploadFilter, PostFilter, PostCommentFilter
)
from .models import (
    FileUpload, Post, PostLike, PostComment, PostCommentLike,
)
from .serializers import (
    FileUploadSerializer, PostSerializer, PostLikeSerializer,
    PostListRetrieveSerializer, PostCreateUpdateDeleteSerializer,
    PostCommentSerializer, PostCommentLikeSerializer
)


# from rest_framework.exceptions import NotFound
# from apps.profiles.models import (
#     Profile,
# )


class FileUploadPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    pagination_class = FileUploadPagination
    filter_class = FileUploadFilter
    parser_classes = (
        parsers.FileUploadParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        queryset = super(FileUploadViewSet, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)

        if self.kwargs.get('username'):
            return queryset.filter(user__user__username=self.kwargs.get('username'))

    def perform_create(self, serializer):
        # try:
        #     user = Profile.objects.get(user__username=self.kwargs.get('username'))
        # except Profile.DoesNotExist:
        #     raise NotFound()
        serializer.save(user=self.request.user.profile)


# Create your views here.
class PostPagination(pagination.PageNumberPagination):
    # page_size = 20
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

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostListRetrieveSerializer
        return PostCreateUpdateDeleteSerializer

    def get_queryset(self):
        # Set up eager loading to avoid N + 1 selects
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        queryset = self.get_serializer_class().annotate_comments_count(queryset)
        queryset = self.get_serializer_class().annotate_likes_dislikes_count(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class PostIdListView(ModelIdListMixin):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_class = PostFilter


class PostLikeMixin(generics.GenericAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def get_queryset(self):
        queryset = super(PostLikeMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(post__id=self.kwargs.get('post__id'))


class PostLikeListCreateView(PostLikeMixin, generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post__id'))
        serializer.save(user=self.request.user.profile, post=post)


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
    filter_class = PostCommentFilter

    def get_queryset(self):
        queryset = super(PostCommentMixin, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(post__id=self.kwargs.get('post__id'))

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post__id'))
        serializer.save(user=self.request.user.profile, post=post)


class PostCommentListCreateView(PostCommentMixin, generics.ListCreateAPIView):
    pass
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(),)


class PostCommentDetailView(PostCommentMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(), IsOwner(),)


class PostCommentLikeListCreateView(generics.ListCreateAPIView):
    queryset = PostCommentLike.objects.all()
    serializer_class = PostCommentLikeSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(
            post_comment__post__id=self.kwargs.get('post__id'),
            post_comment__id=self.kwargs.get('pk')
        )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        post_comment = PostComment.objects.get(id=self.kwargs.get('pk'))
        serializer.save(user=self.request.user.profile, post_comment=post_comment)
