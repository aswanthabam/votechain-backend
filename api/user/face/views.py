from rest_framework.views import APIView
from utils.response import CustomResponse
from utils.face import FaceVerifier, FaceEmbedding
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from db.user import UserFace, UserAuth, UserFaceCache
from django.db.models import Q
import json

class FaceRegistrationAPI(APIView):

    def post(self, request:HttpRequest):
        face_id = request.data.get('face_id')
        image = request.FILES.get('face')
        final = request.data.get('final', False)
        if face_id is None:
            return CustomResponse("Face ID is required!").send_failure_response(400)
        face = UserFace.objects.filter(id=face_id).first()
        if not face:
            return CustomResponse("Invalid Face ID!").send_failure_response(400)
        if face.registered is True:
            return CustomResponse("Face Already Registered!").send_failure_response(400)
        fs = FileSystemStorage()
        name = str(uuid4())
        fs.save(name,image.file)
        url = fs.path(name)
        embeddings = FaceVerifier.get_embeddings(url).tolist()
        fs.delete(name)
        cache = UserFaceCache.objects.filter(face_id=face).first()
        if cache is None:
            cache = UserFaceCache(face_id=face,embedding=json.dumps(embeddings),embeddings=json.dumps([embeddings]))
            cache.save()
        else:
            existing_embeddings = json.loads(str(cache.embeddings))
            existing_embedding = json.loads(str(cache.embedding))
            face_embed = FaceEmbedding(embeddings=existing_embeddings,embedding=existing_embedding)
            status = face_embed.add_embeddings(embeddings)
            if status is False:
                return CustomResponse("Face not consistent!").send_failure_response(400)
            cache.embedding = json.dumps(face_embed.embedding)
            cache.embeddings = json.dumps(face_embed.embeddings)
            cache.save()
        if final:
            face.registered = True
            face.face = json.dumps(face_embed.embedding)
            face.save()
            user = UserAuth.objects.filter(face=face).first()
            user.face_registerd = True
            user.save()
        return CustomResponse("Face Registration API Result",data={
            'status':'success',
            'final':final
        }).send_success_response()

class FaceVerificationAPI(APIView):

    def post(self, request:HttpRequest):
        face = request.FILES.get('face')
        uid = request.data.get('uid')
        if uid is None:
            return CustomResponse("UID is required!").send_failure_response(400)
        user = UserAuth.objects.filter(uid=uid).first()
        if user is None:
            return CustomResponse("User not found!").send_failure_response(400)
        if user.face_registerd is False:
            return CustomResponse("Face not registered!").send_failure_response(400)
        if not face:
            return CustomResponse("No face image found!").send_failure_response(400)
        fs = FileSystemStorage()
        name = str(uuid4())
        fs.save(name,face.file)
        url = fs.path(name)
        embeddings = FaceVerifier.get_embeddings(url)
        fs.delete(name)
        if embeddings is None:
            return CustomResponse("No face found in the image!").send_failure_response(400)
        face_key = user.face.face_key
        user_face:list = json.loads(str(user.face.face))
        result = FaceVerifier.verify_face(embeddings,user_face)
        face_key = face_key if result[0] else None
        return CustomResponse("Face Verification API Result",data={
            'result':result[0],
            'similarity':result[1],
            'absolute':result[2],
            'face_key':face_key
        }).send_success_response()