from rest_framework.views import APIView
from db.models import Constituency, District, State
from .serializer import ConstituencySerializer
from utils.response import CustomResponse
from django.db.models import Q

class ConstituencyListAPIView(APIView):
    def get(self, request):
        constituencies = Constituency.objects.all()
        search = request.GET.get('search')
        if search:
            constituencies = constituencies.filter(Q(name__icontains=search) | Q(code__icontains=search) | Q(description__icontains=search))
        serializer = ConstituencySerializer(constituencies, many=True)
        return CustomResponse('Got Constituencies', serializer.data).send_success_response()

class ConstituencyAPIView(APIView):
    def get(self, request):
        constituency_id = request.GET.get('constituency_id')
        if not constituency_id:
            constituency = Constituency.objects.get(id=constituency_id)
            serializer = ConstituencySerializer(constituency,many=False)
            return CustomResponse('Got Constituency', serializer.data).send_success_response()
        district_id = request.GET.get('district_id')
        state_id = request.GET.get('state_id')
        if not state_id:
            return CustomResponse('State ID not found').send_failure_response(status=400)
        state = State.objects.get(id=state_id)
        if not state:
            return CustomResponse('State not found').send_failure_response(status=400)
        if not district_id:
            return CustomResponse('District ID not found').send_failure_response(status=400)
        district = District.objects.get(id=district_id, state=state)
        if not district:
            return CustomResponse('District not found').send_failure_response(status=400)
        constituencies = Constituency.objects.find(district=district)
        serializer = ConstituencySerializer(constituencies, many=True)
        return CustomResponse('Got Constituencies', serializer.data).send_success_response()

    def post(self, request):
        serializer = ConstituencySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse('Constituency Created', serializer.data).send_success_response(status=200)
        return CustomResponse('Constituency Not Created', serializer.errors).send_failure_response(status=400)
    
    def put(self, request):
        if request.data.get('id'):
            constituency = Constituency.objects.get(id=request.data.get('id'))
            serializer = ConstituencySerializer(instance=constituency, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse('Constituency Updated', serializer.data).send_success_response()
            return CustomResponse('Constituency Not Updated', serializer.errors).send_failure_response(status=400)
        return CustomResponse('Constituency Not Updated').send_failure_response(status=400)
    
    def delete(self, request):
        if request.data.get('id'):
            constituency = Constituency.objects.get(id=request.data.get('id'))
            constituency.delete()
            return CustomResponse('Constituency Deleted').send_success_response()
        return CustomResponse('Constituency Not Deleted').send_failure_response(status=400)