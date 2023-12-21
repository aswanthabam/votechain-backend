from rest_framework.views import APIView
from db.models import District, State
from rest_framework.response import Response
from .serializer import DistrictSerializer
from utils.response import CustomResponse

class DistrictAPIView(APIView):
    def get(self, request):
        district_id = request.GET.get('district_id')
        if not district_id:
            district = District.objects.get(id=district_id)
            serializer = DistrictSerializer(district,many=False)
            return CustomResponse('Got District', serializer.data).send_success_response()
        state_id = request.GET.get('state_id')
        if not state_id:
            return CustomResponse('State ID not found').send_failure_response(status=400)
        state = State.objects.get(id=state_id)
        if not state:
            return CustomResponse('State not found').send_failure_response(status=400)
        districts = District.objects.find(state=state)
        serializer = DistrictSerializer(districts, many=True)
        return CustomResponse('Got Districts', serializer.data).send_success_response()

    def post(self, request):
        serializer = DistrictSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse('District Created', serializer.data).send_success_response(status=200)
        return CustomResponse('District Not Created', serializer.errors).send_failure_response(status=400)
    
    def put(self, request):
        if request.data.get('id'):
            district = District.objects.get(id=request.data.get('id'))
            serializer = DistrictSerializer(instance=district, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse('District Updated', serializer.data).send_success_response()
            return CustomResponse('District Not Updated', serializer.errors).send_failure_response(status=400)
        return CustomResponse('District Not Updated').send_failure_response(status=400)
    
    def delete(self, request):
        if request.data.get('id'):
            district = District.objects.get(id=request.data.get('id'))
            district.delete()
            return CustomResponse('District Deleted').send_success_response()
        return CustomResponse('District Not Deleted').send_failure_response(status=400)