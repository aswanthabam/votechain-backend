from django.urls import path, include

urlpatterns = [
    path("system/", include("api.system.urls")),
    path("location/", include("api.location.urls")),
    path("web3/", include("api.web3.urls"))
]
