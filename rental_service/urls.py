from .views import ListBooksView

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("api/v1/books/search", ListBooksView.as_view(), name="list-book"),
]
