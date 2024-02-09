from django.urls import path

from .views import ReallocateAppIDView, GetAccessKey

urlpatterns = [
    path('reallocate-id/',ReallocateAppIDView.as_view()),
    path('get-access-key/',GetAccessKey.as_view()),
]
