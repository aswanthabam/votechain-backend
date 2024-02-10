from rest_framework.views import APIView
from utils.response import CustomResponse
from db.user import UserAuth, random_hex, AccessKey, AppInstance
from utils.encryption import decrypt, encrypt
from utils.security import require_app_key
class ReallocateAppIDView(APIView):

    def post(self, request):
        try:
            uid = request.data.get('uid')
            if uid is None:
                return CustomResponse("UID is required!").send_failure_response(400)
            user = UserAuth.objects.filter(uid=uid).first()
            if user is None:
                return CustomResponse("User not found!").send_failure_response(400)
            security_hash = request.data.get('security_hash')
            if security_hash is None:
                return CustomResponse("An error Occured (1)").send_failure_response(400)
            security_hash_result = decrypt(security_hash, user.face.face_key)
            if security_hash_result != uid:
                return CustomResponse("An error occured (2)").send_failure_response(400)
            app_key = random_hex()
            user.app_key = app_key
            user.save()
            return CustomResponse("App Key Reallocated",data={
                'app_key':encrypt(app_key, user.face.face_key)
            }).send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("An error occured (3)").send_failure_response(500)


class GetAccessKey(APIView):
    @require_app_key
    def post(self, request):
        try:
            user = request.user
            if user is None:
                return CustomResponse("User not found!").send_failure_response(400)
            clientId = request.data.get('clientId')
            if clientId is None:
                return CustomResponse("Client ID is required!").send_failure_response(400)
            uid = request.user.uid
            print(uid)
            scope = request.data.get('scope')
            if scope is None:
                return CustomResponse("Scope is required!").send_failure_response(400)
            old_keys = AccessKey.objects.filter(userId=user,clientId=clientId,scope=scope).first()
            if old_keys:
                return CustomResponse("Access Key Already Created",data={
                    'access_key':old_keys.key
                }).send_success_response()
            key = random_hex()
            access_key = AccessKey.objects.create(userId=user,key=key,scope=scope,clientId=clientId)
            return CustomResponse("Access Key Created",data={
                'access_key':key
            }).send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("An error occured").send_failure_response(500)
    
    @require_app_key
    def get(self,request):
        try:
            user = request.user
            clientId = request.GET.get('clientId')
            if clientId is None:
                return CustomResponse("Client ID is required!").send_failure_response(400)
            if user is None:
                return CustomResponse("User not found!").send_failure_response(400)
            key = AccessKey.objects.filter(userId=user,clientId=clientId).first()
            if key is None:
                return CustomResponse("No access keys found!",data={
                    'has_access_key':False
                }).send_failure_response(400)
            
            return CustomResponse("Access Key",data={
                'has_access_key':True,
                'access_key':key.key
            }).send_success_response()
        
        except Exception as e:
            print(e)
            return CustomResponse("An error occured").send_failure_response(500)