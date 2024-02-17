from rest_framework.views import APIView
from utils.response import CustomResponse
from .serializers import ElectionStatisticesSerializer
from db.election import ElectionStatistices
from utils.security import require_app_key

class ElectionStatisticsAPI(APIView):

    def get(self, request):
        electionId = request.GET.get('electionId')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        elections = ElectionStatistices.objects.filter(election=electionId)
        if start_time:
            elections = elections.filter(time__gte=start_time)
        if end_time:
            elections = elections.filter(time__lte=end_time)
        serializer = ElectionStatisticesSerializer(elections, many=True)
        return CustomResponse(message="Election statistics",data=serializer.data, status=200)
    
    @require_app_key
    def post(self, request):
        try:
            election = request.data.get('election')
            if not election:
                return CustomResponse(message="Election is required",data={}).send_failure_response(400)
            if not request.user:
                return CustomResponse(message="User not found",data={}).send_failure_response(400)
            if ElectionStatistices.objects.filter(user=request.user.id, election= int( election)).first():
                return CustomResponse(message="Already voted",data={}).send_failure_response(400)
            request_data = {
                'election': election,
                'user': request.user.id

            }
            serializer = ElectionStatisticesSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(message="Added vote",data=serializer.data).send_success_response(200)
            return CustomResponse(message="Error occured",data=serializer.errors).send_failure_response(400)
        except Exception as e:
            print(e)
            return CustomResponse(message="Error occured",data=str(e)).send_failure_response(500)