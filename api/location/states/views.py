from rest_framework.views import APIView
from db.models import District, State
from .serializer import StateSerializer
from utils.response import CustomResponse
from django.db.models import Q
class StateListAPIView(APIView):
    def get(self, request):
        states = State.objects.all()
        search = request.GET.get('search')
        if search:
            states = states.filter(Q(name__icontains=search) | Q(code__icontains=search))
        serializer = StateSerializer(states, many=True)
        return CustomResponse('Got States', serializer.data).send_success_response()

class StateAPIView(APIView):
    def get(self, request):
        state_id = request.GET.get('state_id')
        if not state_id:
            state = State.objects.get(id=state_id)
            serializer = StateSerializer(state,many=False)
            return CustomResponse('Got State', serializer.data).send_success_response()
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return CustomResponse('Got States', serializer.data).send_success_response()

    def post(self, request):
        serializer = StateSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse('State Created', serializer.data).send_success_response(status=200)
        return CustomResponse('State Not Created', serializer.errors).send_failure_response(status=400)
    
    def put(self, request):
        if request.data.get('id'):
            state = State.objects.get(id=request.data.get('id'))
            serializer = StateSerializer(instance=state, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse('State Updated', serializer.data).send_success_response()
            return CustomResponse('State Not Updated', serializer.errors).send_failure_response(status=400)
        return CustomResponse('State Not Updated').send_failure_response(status=400)
    
    def delete(self, request):
        if request.data.get('id'):
            state = State.objects.get(id=request.data.get('id'))
            state.delete()
            return CustomResponse('State Deleted').send_success_response()
        return CustomResponse('State Not Deleted').send_failure_response(status=400)