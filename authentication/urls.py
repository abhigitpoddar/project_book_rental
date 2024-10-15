from .views import CreateUserView

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("api/v1/signup", CreateUserView.as_view(), name="user-creation"),
]
