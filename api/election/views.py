from rest_framework.views import APIView
from utils.response import CustomResponse
from .serializers import ElectionStatisticesSerializer
from db.election import ElectionStatistices
from utils.security import require_app_key
from datetime import datetime
from datetime import timedelta

class ElectionStatisticsAPI(APIView):

    def get(self, request):
        try:
            election = request.GET.get('election')
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            response_type = request.GET.get('type','individual') # individual or time
            gap : str= request.GET.get('gap','hour') # hour, minute, seconds
            if not election:
                return CustomResponse(message="Election is required",data={}).send_failure_response(400)
            elections = ElectionStatistices.objects.filter(election=election)

            if start_time:
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                elections = elections.filter(time__gte=start_time)
            if end_time:
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                elections = elections.filter(time__lte=end_time)
            if response_type == 'time':
                start_time : datetime = start_time if start_time else ElectionStatistices.objects.filter(election=election).order_by('time').first().time
                end_time : datetime = end_time if end_time else ElectionStatistices.objects.filter(election=election).order_by('-time').first().time
                cur_gap = start_time
                data = {}
                print(gap, cur_gap, end_time)
                while cur_gap <= end_time:
                    print(cur_gap)
                    next_gap = cur_gap + (timedelta(hours=1) if gap == 'hour' else (timedelta(minutes=1) if gap == 'minute' else timedelta(seconds=1)))
                    votes = elections.filter(time__gte=cur_gap, time__lte=next_gap).count()
                    data[cur_gap.strftime('%Y-%m-%d %H:%M:%S')] = votes
                    cur_gap = next_gap
                return CustomResponse(message="Election statistics",data=data).send_success_response(200)
            serializer = ElectionStatisticesSerializer(elections, many=True)
            return CustomResponse(message="Election statistics",data=serializer.data).send_success_response(200)
        except Exception as e:
            print(e)
            return CustomResponse(message="Error occured",data=str(e)).send_failure_response(500)
    
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