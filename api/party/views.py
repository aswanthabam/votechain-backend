from rest_framework.views import APIView
from .serializers import PartySerializers
from utils.response import CustomResponse
from db.candidate import Party
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
class PartyAPI(APIView):

    def get(self, request):
        partyId = request.GET.get('partyId')
        if partyId is not None:
            party = Party.objects.filter(id=partyId).first()
            if party is None:
                return CustomResponse(message="Party not found",data={}).send_failure_response()
            serializer = PartySerializers(party,many=False)
            return CustomResponse(message="Party found",data=serializer.data).send_success_response()
        parties = Party.objects.all()
        serializer = PartySerializers(parties, many=True)
        return CustomResponse(message="List of parties",data=serializer.data).send_success_response()

    def post(self, request):
        try:
            logo = request.FILES.get('logo')
            if logo is None:
                return CustomResponse("Logo is required!").send_failure_response()
            fs = FileSystemStorage()
            path_name = f'party/logo/{uuid4()}.jpg'
            fs.save(path_name,logo)
            url = fs.url(path_name)
            request_data = {
                "logo":url,
                'name':request.data.get('name')
            }
            serializer = PartySerializers(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(message="Successfuly saved party",data=serializer.data).send_success_response()
            return CustomResponse(message="Failed to save party",data=serializer.errors).send_failure_response()
        except Exception as e:
            print(e)
            return CustomResponse("Error occured").send_failure_response(500)