from rest_framework.views import APIView
from utils.response import CustomResponse
from api.apps import FaceConfig
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from db.user import UserFace, UserAuth
from django.db.models import Q
import json

class FaceRegistrationAPI(APIView):
    def post(self, request:HttpRequest):
        face = request.FILES.get('face')
        uid = request.data.get('uid')
        user = UserAuth.objects.filter(uid=uid).first()
        if user is None:
            return CustomResponse("User not found!").send_failure_response(400)
        if uid is None:
            return CustomResponse("UID is required!").send_failure_response(400)
        user_face = UserFace.objects.filter(Q(userAuth__uid=uid)).first()
        if user_face is not None:
            return CustomResponse("User already registered!").send_failure_response(400)
        if not face:
            return CustomResponse("No face image found!").send_failure_response(400)
        fs = FileSystemStorage()
        name = str(uuid4())
        fs.save(name,face.file)
        url = fs.path(name)
        print(url)
        embeddings = FaceConfig.get_face_embeddings(url)
        if embeddings is None:
            fs.delete(name)
            return CustomResponse("No face found in the image!").send_failure_response(400)
        fs.delete(name)
        try:
            UserFace.objects.create(userAuth=user,face=json.dumps(list(embeddings)))
            return CustomResponse("Face Registered Successfuly").send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while registering face!").send_failure_response(500)

class FaceVerificationAPI(APIView):
    def post(self, request:HttpRequest):
        face = request.FILES.get('face')
        uid = request.data.get('uid')
        if uid is None:
            return CustomResponse("UID is required!").send_failure_response(400)
        user_face = UserFace.objects.filter(Q(userAuth__uid=uid)).first()
        if user_face is None:
            return CustomResponse("User not found!").send_failure_response(400)
        if not face:
            return CustomResponse("No face image found!").send_failure_response(400)
        fs = FileSystemStorage()
        name = str(uuid4())
        fs.save(name,face.file)
        url = fs.path(name)
        print(url)
        embeddings = FaceConfig.get_face_embeddings(url)
        fs.delete(name)
        if embeddings is None:
            fs.delete(name)
            return CustomResponse("No face found in the image!").send_failure_response(400)
        user_face:list = json.loads(str(user_face.face))
        result = FaceConfig.verify_face(embeddings,user_face)
        return CustomResponse("Face Verification API Result",data={'result':result}).send_success_response()