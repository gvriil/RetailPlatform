# network/pagination.py
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination for API results.
    Allows client to control page size via query parameter.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
