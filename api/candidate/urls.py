from django.urls import path
from .views import CandidateProfileRegisterAPI, CandidateEducationAPI, CandidateExperienceAPI
urlpatterns = [
    path('register/',CandidateProfileRegisterAPI.as_view(),name='candidate-register'),
    path('profile/',CandidateProfileRegisterAPI.as_view(),name='candidate-profile'),
    path('education/add/',CandidateEducationAPI.as_view(),name='candidate-education'),
    path('experience/add/',CandidateExperienceAPI.as_view(),name='candidate-experience'),
]
