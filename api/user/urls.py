from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.user.auth.urls")),
]
