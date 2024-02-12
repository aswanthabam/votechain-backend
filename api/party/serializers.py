from rest_framework import serializers
from db.candidate import Party

class PartySerializers(serializers.ModelSerializer):
    partyId = serializers.CharField(read_only=True, source='id')
    
    class Meta:
        model = Party
        fields = [
            'partyId',
            'name',
            'logo'
        ]