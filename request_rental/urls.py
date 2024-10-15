from .views import CreateRequestsView

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("api/v1/request/create", CreateRequestsView.as_view(), name="create-rental-request"),
]
