from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Tamaño de página por defecto
    page_size_query_param = 'page_size'  # Nombre del parámetro de consulta para el tamaño de página
    max_page_size = 100  # Tamaño de página máximo