from django.contrib import admin
from django.urls import path, include
from .views import SystemConfigAPIView

urlpatterns = [
    path("config/", SystemConfigAPIView.as_view()),
]
