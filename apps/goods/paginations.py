from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15


class GoodsPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15
