from django.urls import path, include
from .views import EthersFundView
urlpatterns = [
    path("fund/", EthersFundView.as_view()),
]
