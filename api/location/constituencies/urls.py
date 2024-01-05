from django.urls import path, include
from .views import ConstituencyAPIView, ConstituencyListAPIView
urlpatterns = [
    path("", ConstituencyAPIView.as_view()),
    path("list/", ConstituencyListAPIView.as_view()),
]
