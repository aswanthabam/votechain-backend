from django.urls import path, include
from .views import StateAPIView
urlpatterns = [
    path("", StateAPIView.as_view()),
]
