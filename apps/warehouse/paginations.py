from rest_framework.pagination import PageNumberPagination


class WarehousePagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15


class InventoryPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class FlowPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class CountingListPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class RequisitionPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15



class StockInOrderPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15
