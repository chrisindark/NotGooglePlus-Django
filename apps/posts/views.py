from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from apps.core.mixins import ReadOnlyIdListMixin
from apps.core.serializers import ReadOnlyIdSerializer
from apps.posts.pagination import PostPagination
from apps.posts.permissions import IsPostOwner
from apps.profiles.models import Profile

from .filters import PostFilter
from .models import Post
from .serializers import (
    PostCreateUpdateDeleteSerializer,
    PostListRetrieveSerializer,
    PostSerializer,
)


# Create your views here.
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

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_class = PostFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [
                permissions.AllowAny(),
            ]
        return [
            permissions.IsAuthenticated(),
            IsPostOwner(),
        ]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostListRetrieveSerializer
        return PostCreateUpdateDeleteSerializer

    def get_queryset(self):
        # Set up eager loading to avoid N + 1 selects
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        # queryset = self.get_serializer_class().annotate_comments_count(queryset)
        # queryset = self.get_serializer_class().annotate_likes_dislikes_count(queryset)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(profile=profile)


class PostIdListView(ReadOnlyIdListMixin, generics.ListAPIView):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_class = PostFilter
    serializer_class = ReadOnlyIdSerializer
