from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.user.auth.urls")),
    path("face/", include("api.user.face.urls")),
]
