from django.urls import path, include
from .views import AuthAPIRegisterView,AuthAPILoginView
urlpatterns = [
    path('register/',AuthAPIRegisterView.as_view()),
    path('login/',AuthAPILoginView.as_view()),
]
