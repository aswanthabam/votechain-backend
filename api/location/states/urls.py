from django.urls import path, include
from .views import StateAPIView, StateListAPIView
urlpatterns = [
    path("", StateAPIView.as_view()),
    path("list/", StateListAPIView.as_view()),
]
