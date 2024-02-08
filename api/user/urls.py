from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.user.auth.urls")),
    path("app/", include("api.user.app.urls")),
    path("face/", include("api.user.face.urls")),
]
