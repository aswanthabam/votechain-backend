from django.urls import path, include
from .views import ConstituencyAPIView
urlpatterns = [
    path("", ConstituencyAPIView.as_view()),
]
