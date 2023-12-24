from rest_framework.views import APIView
from utils.response import CustomResponse
from .serializer import UserAuthSerializer
from db.user import UserAuth

class AuthAPILoginView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('uid')
            aadhar = request.data.get('aadhar')
            if user_id is None and aadhar is None:
                return CustomResponse("The entered UID or aadhar is not correct!").send_failure_response(400)
            if user_id is not None:
                user = UserAuth.objects.filter(uid=user_id).first()
            elif aadhar is not None:
                user = UserAuth.objects.filter(aadhar=aadhar).first()
            if user is None:
                return CustomResponse("The entered UID or aadhar is not correct!").send_failure_response(400)

            return CustomResponse(
                message="Auth",
                data={
                    'ec1': user.enc1,
                    'ec2': user.enc2
                }
            ).send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while authenticating user!").send_failure_response(500)

class AuthAPIRegisterView(APIView):
    def post(self, request):
        try:
            userAuth = UserAuth.objects.filter(uid=request.data.get('uid')).first()
            if userAuth is not None:
                return CustomResponse("The entered UID is already registered!").send_failure_response(400)
            serializer = UserAuthSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    message="Auth",
                    data={
                        'message': 'Auth',
                        'data': serializer.data
                    }
                ).send_success_response()
            
            return CustomResponse("Error Occured while authenticating user!",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while authenticating user!").send_failure_response(500)