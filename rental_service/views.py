from .models import Book
from .serializers import BookSerializer

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from django.db.models.query import QuerySet
from django.shortcuts import render


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self) -> QuerySet:
        book_name = self.request.query_params.get('name')
        queryset = Book.objects.filter(name__icontains=book_name)
        return queryset
