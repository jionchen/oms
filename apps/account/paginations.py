from rest_framework.pagination import PageNumberPagination


class AccountPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15


class BookkeepingPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20


class UserPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15
