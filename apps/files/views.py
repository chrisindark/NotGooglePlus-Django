from rest_framework import pagination, viewsets, parsers, permissions, mixins
from rest_framework.exceptions import MethodNotAllowed

from apps.accounts.permissions import IsOwner

from .models import FileUpload
from .filters import FileUploadFilter
from .serializers import FileUploadSerializer


# Create your views here.
class FileUploadPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'


class FileUploadViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    pagination_class = FileUploadPagination
    filter_class = FileUploadFilter
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def get_queryset(self):
        queryset = super(FileUploadViewSet, self).get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
        # if self.kwargs.get('username'):
        #     return queryset.filter(user__user__username=self.kwargs.get('username'))

    def perform_create(self, serializer):
        # try:
        #     user = Profile.objects.get(user__username=self.kwargs.get('username'))
        # except Profile.DoesNotExist:
        #     raise NotFound()
        serializer.save(user=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed
