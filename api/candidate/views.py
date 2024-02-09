from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from .serializers import CandidateProfileSerializer, CandidateEducationSerializer, CandidateExperienceSerializer
from utils.response import CustomResponse
from db.candidate import CandidateProfile
from django.http import QueryDict
from uuid import uuid4
class CandidateProfileRegisterAPI(APIView):
    def get(self,request):
        candidateId = request.GET.get('candidateId')
        if candidateId is None:
            return CustomResponse("Candidate ID is required!").send_failure_response(400)
        candidate = CandidateProfile.objects.filter(candidateId=candidateId).first()
        if candidate is None:
            return CustomResponse("Invalid Candidate ID!").send_failure_response(400)
        serializer = CandidateProfileSerializer(candidate,many=False,partial=True)
        return CustomResponse(
            message="Profile",
            data={**serializer.data}
        ).send_success_response()
    def post(self,request):
        try:
            photo = request.FILES.get('photo')
            
            if photo is None:
                return CustomResponse("Photo is required!").send_failure_response(400)
            fs = FileSystemStorage()
            name = fs.save(f'{uuid4()}.jpg',photo)
            url = fs.url(name)

            request_data = {
                'photo': url,
                'candidateId': request.data.get('candidateId'),
                'about': request.data.get('about')
            }
            
            serializer = CandidateProfileSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    message="Profile",
                    data={**serializer.data}
                ).send_success_response()
            else:
                return CustomResponse("Error Occured while registering profile!",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while registering profile!").send_failure_response(500)

    def put(self,request):
        try:
            candidateId = request.data.get('candidateId')
            if candidateId is None:
                return CustomResponse("Candidate ID is required!").send_failure_response(400)
            candidate = CandidateProfile.objects.filter(candidateId=candidateId).first()
            if candidate is None:
                return CustomResponse("Invalid Candidate ID!").send_failure_response(400)
            photo = request.FILES.get('photo')
            if photo:
                fs = FileSystemStorage()
                name = fs.save(f'{uuid4()}.jpg',photo)
                url = fs.url(name)
                request_data = {
                    'photo': url,
                    'about': request.data.get('about') 
                }
                serializer = CandidateProfileSerializer(instance=candidate,data=request_data,many=False,partial=True)
            else:
                request_data = {
                    'about': request.data.get('about') 
                }
                serializer = CandidateProfileSerializer(instance=candidate,data=request_data,many=False,partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    message="Profile",
                    data={**serializer.data}
                ).send_success_response()
            else:
                return CustomResponse("Error Occured while registering profile!",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while registering profile!").send_failure_response(500)
        
class CandidateEducationAPI(APIView):
    def post(self,request):
        try:
            serializer = CandidateEducationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    message="Education",
                    data={**serializer.data}
                ).send_success_response()
            else:
                return CustomResponse("Error Occured while registering education!",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while registering education!").send_failure_response(500)
class CandidateExperienceAPI(APIView):
    def post(self,request):
        try:
            serializer = CandidateExperienceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    message="Experience",
                    data={**serializer.data}
                ).send_success_response()
            else:
                return CustomResponse("Error Occured while registering education!",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while registering education!").send_failure_response(500)
        
        