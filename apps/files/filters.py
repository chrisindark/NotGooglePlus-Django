import django_filters

from apps.posts.filters import PostFilter
from .models import FileUpload


class FileUploadFilter(django_filters.FilterSet):
    # class Meta(PostFilter.Meta):
    #     model = FileUpload
    username = django_filters.CharFilter(name='user__user__username')
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = FileUpload
        fields = ('created_at',)
