import django_filters
from .models import *

class PostFilter(django_filters.rest_framework.FilterSet):
    # user_id = django_filters.CharFilter(name="user__id")
    # user_email = django_filters.CharFilter(name="user__email")
    # user_username = django_filters.CharFilter(name="user__username")

    class Meta:
        model = Post
        fields = (
            'user__username',
            'created_at',
            # 'user_id',
            # 'user_email',
            # 'user_username',
        )
        order_by = (
            'created_at',
            '-created_at',
        )


class CommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Comment
        fields = (
            'post__id',
            'created_at',
        )
        order_by = (
            'created_at',
            '-created_at',
        )

class FIleUploadFilter(django_filters.rest_framework.FilterSet):
    class Meta(PostFilter.Meta):
        model = FileUpload
