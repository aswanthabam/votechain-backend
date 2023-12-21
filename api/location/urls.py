from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("districts/", include("api.location.districts.urls")),
    path("states/", include("api.location.states.urls")),
    path("constituencies/", include("api.location.constituencies.urls")),
]
