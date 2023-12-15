from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import SystemConfigSerializer
from db.models import SystemConfig
from utils.response import CustomResponse

class SystemConfigAPIView(APIView):
    def get(self, request):
        system_configs = SystemConfig.objects.all()
        serializer = SystemConfigSerializer(system_configs, many=True)
        if not serializer.data or not len(serializer.data) > 0:
            return CustomResponse('System Configs Not Found', serializer.data).send_failure_response(status=status.HTTP_404_NOT_FOUND)
        return CustomResponse('System Configs', serializer.data).send_success_response()

    def post(self, request):
        SystemConfig.objects.all().delete()
        serializer = SystemConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse('System Config Created', serializer.data).send_success_response(status=status.HTTP_201_CREATED)
        return CustomResponse('System Config Not Created', serializer.errors).send_failure_response(status=status.HTTP_400_BAD_REQUEST)
    
