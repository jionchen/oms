from rest_framework.pagination import PageNumberPagination


class SupplierPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 15


class PurchaseOrderPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class PurchasePriceRecordPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20


class PurchasePaymentRecordPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10
