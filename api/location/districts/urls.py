from django.urls import path, include
from .views import DistrictAPIView
urlpatterns = [
    path("", DistrictAPIView.as_view()),
]
