from rest_framework.views import APIView
from utils.response import CustomResponse
from db.user import UserAuth, random_hex
from utils.encryption import decrypt, encrypt

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

        