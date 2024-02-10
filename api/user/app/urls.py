from django.urls import path

from .views import ReallocateAppIDView, GetAccessKey

urlpatterns = [
    path('reallocate-id/',ReallocateAppIDView.as_view()),
    path('get-accesskey/',GetAccessKey.as_view()),
    path('is-accesskey-available/',GetAccessKey.as_view(),name='is-access-key-available'),
]
