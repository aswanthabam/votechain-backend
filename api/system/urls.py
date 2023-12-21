from django.urls import path
from .views import SystemConfigAPIView

urlpatterns = [
    path("config/", SystemConfigAPIView.as_view()),
]
