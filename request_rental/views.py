from .serializers import RequestSerializer

from django.shortcuts import render
from rest_framework import generics, permissions, status


# Create your views here.
class CreateRequestsView(generics.CreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: RequestSerializer) -> None:
        serializer.save(user=self.request.user)
