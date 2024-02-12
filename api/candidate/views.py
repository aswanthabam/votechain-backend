from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from .serializers import CandidateProfileSerializer, CandidateEducationSerializer, CandidateExperienceSerializer
from utils.response import CustomResponse
from db.candidate import CandidateProfile, CandidateDocumentLinker, Document
from db.user import UserAuth, AccessKey
from uuid import uuid4
from django.http import HttpRequest
from utils.security import require_access_key
from utils.types import AccessKeyScope
class CandidateProfileRegisterAPI(APIView):
    def get(self,request):
        accessKey = request.GET.get('ACCESS_KEY')
        candidateAddress = request.GET.get('candidateAddress')
        if accessKey is not None and candidateAddress is None:
            accessKey = AccessKey.objects.filter(key=accessKey).first()
            if accessKey is None:
                return CustomResponse("Invalid Access Key!").send_failure_response(400)
            candidate = CandidateProfile.objects.filter(userId=accessKey.userId.id).first()
            if candidate is None:
                return CustomResponse("Profile not found (2)!").send_failure_response(400)
            serializer = CandidateProfileSerializer(candidate,many=False,partial=True)
            return CustomResponse(
                message="Profile",
                data={**serializer.data,'party':{
                    'partyId':candidate.party.id,
                    'name':candidate.party.name,
                    'logo':candidate.party.logo
                }}
            ).send_success_response()
        if candidateAddress is None:
            return CustomResponse("Candidate Address is required!").send_failure_response(400)
        candidate = CandidateProfile.objects.filter(candidateAddress=candidateAddress).first()
        if candidate is None:
            return CustomResponse("Invalid Candidate Address!").send_failure_response(400)
        serializer = CandidateProfileSerializer(candidate,many=False,partial=True)
        return CustomResponse(
            message="Profile",
            data={**serializer.data,'party':{
                    'partyId':candidate.party.id,
                    'name':candidate.party.name,
                    'logo':candidate.party.logo
                }}
        ).send_success_response()
    
    @require_access_key(AccessKeyScope.CANDIDATE_PROFILE.value)
    def post(self,request):
        try:
            if request.candidate is not None:
                return CustomResponse("Profile already exists!").send_failure_response(400)
            if request.user is None:
                return CustomResponse("User not found, Invalid access key!").send_failure_response(400)
            photo = request.FILES.get('photo')
            url = None
            if photo is not None:
                fs = FileSystemStorage()
                name = fs.save(f'candidate/photos/{uuid4()}.jpg',photo)
                url = fs.url(name)
            user = request.user
            if user is None:
                return CustomResponse("Invalid UID!").send_failure_response(400)
            name = request.data.get('name')
            
            if name is None:
                return CustomResponse("Name is required!").send_failure_response(400)
            request_data = {
                'photo': url,
                'candidateAddress': request.data.get('candidateAddress'),
                'about': request.data.get('about'),
                "userId":user.id,
                "name":name,
                "phone":request.data.get('phone'),
                "email":request.data.get('email'),
                "address":request.data.get('address'),
                "party":request.data.get('party'),
                "logo":request.data.get('logo')
            }
            print(request_data)
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
                name = fs.save(f'candidate/photos/{uuid4()}.jpg',photo)
                url = fs.url(name)
                request_data = {
                    'photo': url,
                    'about': request.data.get('about',candidate.about),
                    'name': request.data.get('name',candidate.name) ,
                    'phone': request.data.get('phone',candidate.phone),
                    'email': request.data.get('email',candidate.email),
                    'address': request.data.get('address',candidate.address),
                    'party': request.data.get('party',candidate.party.id),
                    'logo': request.data.get('logo',candidate.logo)
                    
                }
                serializer = CandidateProfileSerializer(instance=candidate,data=request_data,many=False,partial=True)
            else:
                request_data = {
                    'about': request.data.get('about',candidate.about) ,
                    'name': request.data.get('name',candidate.name),
                    'phone': request.data.get('phone',candidate.phone),
                    'email': request.data.get('email',candidate.email),
                    'address': request.data.get('address',candidate.address),
                    'party': request.data.get('party',candidate.party.id),
                    'logo': request.data.get('logo',candidate.logo)

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
                'fromWhere': request.data.get('fromWhere')
            }
            serializer = CandidateEducationSerializer(data=request_data,context={'candidate':candidate})
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
            }
            serializer = CandidateExperienceSerializer(data=request_data,context={'candidate':candidate})
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