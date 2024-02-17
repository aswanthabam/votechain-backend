from django.urls import path, include
from .views import ElectionStatisticsAPI
urlpatterns = [
    path('add-vote/', ElectionStatisticsAPI.as_view(), name="add-vote"),
]
