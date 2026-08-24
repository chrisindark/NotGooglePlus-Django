from rest_framework import pagination


class TagPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 500
