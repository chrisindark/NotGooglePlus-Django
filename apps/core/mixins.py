from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class ReadOnlyIdListMixin:
    """
    Returns only list of IDs from queryset.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.values_list("id", flat=True)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = [key["id"] for key in serializer.data]
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = [key["id"] for key in serializer.data]

        return Response(data)


class BulkCreateModelMixin:
    """
    Allow a view to accept either:
    - a single object payload for normal create, or
    - a list payload for bulk create.
    """

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        if isinstance(serializer.validated_data, list):
            # skips calling .save() and skips signals
            self.get_queryset().model.objects.bulk_create(
                [
                    self.get_queryset().model(**item)
                    for item in serializer.validated_data
                ]
            )
        else:
            serializer.save()
