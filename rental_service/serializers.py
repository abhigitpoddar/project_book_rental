from .models import Book, Rental

from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Book
        fields = "__all__"
