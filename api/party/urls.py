from django.urls import path
from .views import PartyAPI
urlpatterns = [
    path('add/',PartyAPI.as_view(),name='party-add'),
    path('get/',PartyAPI.as_view(),name='party-get'),
]
