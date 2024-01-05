from django.urls import path, include
from .views import DistrictAPIView, DistrictListAPIView
urlpatterns = [
    path("", DistrictAPIView.as_view()),
    path("list/", DistrictListAPIView.as_view()),
]
