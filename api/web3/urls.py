from django.urls import path, include

urlpatterns = [
    path("ethers/", include("api.web3.ethers.urls")),
]
