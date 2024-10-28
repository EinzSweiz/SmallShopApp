from rest_framework.pagination import PageNumberPagination


class StandartResultsSetPagination(PageNumberPagination):
    page_size = 5  # Set a default page size of 15
    page_size_query_param = 'limit'
    max_page_size = 10  # You can adjust the max limit
