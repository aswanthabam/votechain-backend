from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("system/", include("api.system.urls")),
]
