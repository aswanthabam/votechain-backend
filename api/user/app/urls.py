from django.urls import path

from .views import ReallocateAppIDView
urlpatterns = [
    path('reallocate-id/',ReallocateAppIDView.as_view())
]
