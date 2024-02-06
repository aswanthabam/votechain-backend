from django.urls import path
from .views import *
urlpatterns = [
    path('verify/', FaceVerificationAPI.as_view(), name='face-verify'),
    path('register/', FaceRegistrationAPI.as_view(), name='face-register')
]
