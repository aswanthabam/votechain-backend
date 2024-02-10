from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from .serializers import CandidateProfileSerializer, CandidateEducationSerializer, CandidateExperienceSerializer
from utils.response import CustomResponse
from db.candidate import CandidateProfile, CandidateDocumentLinker, Document
from db.user import UserAuth
from uuid import uuid4
from django.http import HttpRequest
from utils.security import require_access_key
from utils.types import AccessKeyScope
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
    
    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def post(self,request):
        try:
            if request.candidate is not None:
                return CustomResponse("Profile already exists!").send_failure_response(400)
            if request.user is None:
                return CustomResponse("User not found, Invalid access key!").send_failure_response(400)
            photo = request.FILES.get('photo')
            if photo is None:
                return CustomResponse("Photo is required!").send_failure_response(400)
            fs = FileSystemStorage()
            name = fs.save(f'candidate/photos/{uuid4()}.jpg',photo)
            url = fs.url(name)
            uid = request.data.get('uid')
            if uid is None:
                return CustomResponse("UID is required!").send_failure_response(400)
            user = UserAuth.objects.filter(uid=uid).first()
            if user is None:
                return CustomResponse("Invalid UID!").send_failure_response(400)
            
            request_data = {
                'photo': url,
                'candidateId': request.data.get('candidateId'),
                'about': request.data.get('about'),
                "userId":user.id
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

    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def put(self,request):
        try:
            candidate = request.candidate
            if candidate is None:
                return CustomResponse("Candidate Profile doen't exists!").send_failure_response(400)
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
    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def post(self,request):
        try:
            candidate = request.candidate
            if candidate is None:
                return CustomResponse("Candidate Profile doen't exists!").send_failure_response(400)
            request_data = {
                'title': request.data.get('title'),
                'description': request.data.get('description'),
                'fromWhere': request.data.get('fromWhere'),
                'candidateId': candidate.candidateId
            }
            serializer = CandidateEducationSerializer(data=request_data)
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
    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def post(self,request):
        try:
            candidate = request.candidate
            if candidate is None:
                return CustomResponse("Candidate Profile doen't exists!").send_failure_response(400)
            request_data = {
                'title': request.data.get('title'),
                'description': request.data.get('description'),
                'fromWhere': request.data.get('fromWhere'),
                'candidateId': candidate.candidateId
            }
            serializer = CandidateExperienceSerializer(data=request_data)
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
        
class CandidateDocumentUpload(APIView):
    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def post(self,request:HttpRequest):
        try:
            
            candidate = request.candidate
            if candidate is None:
                return CustomResponse("Candidate Profile doen't exists!").send_failure_response(400)
            document = request.FILES.get('document')
            if document is None:
                return CustomResponse("Document is required!").send_failure_response(400)
            title = request.data.get('title')
            if title is None:
                return CustomResponse("Document Title is required!").send_failure_response(400)
            fs = FileSystemStorage()
            docType = document.name.split('.')
            docType = docType[-1] if len(docType) > 1 else 'pdf'
            name = fs.save(f'candidate/documents/{uuid4()}.{docType}',document)
            url = fs.url(name)
            document = Document.objects.create(title=title,link=url)
            CandidateDocumentLinker.objects.create(candidate=candidate,document=document)
            return CustomResponse(
                message="Document",
                data={'document': url}
            ).send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while uploading document!").send_failure_response(500)