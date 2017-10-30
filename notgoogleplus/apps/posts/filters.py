import django_filters

from .models import *


class PostFilter(django_filters.FilterSet):
    # user_id = django_filters.CharFilter(name="user__id")
    # user_email = django_filters.CharFilter(name="user__email")
    # user_username = django_filters.CharFilter(name="user__username")

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created_at', 'created_at'),
        ),
    )
    class Meta:
        model = Post
        fields = (
            'user__username',
            'created_at',
            # 'user_id',
            # 'user_email',
            # 'user_username',
        )


class PostCommentFilter(django_filters.FilterSet):
    class Meta:
        model = PostComment
        fields = (
            'post__id',
            'created_at',
        )
        order_by = (
            'created_at',
            '-created_at',
        )


class FileUploadFilter(django_filters.FilterSet):
    class Meta(PostFilter.Meta):
        model = FileUpload
