from rest_framework import serializers
from db.election import ElectionStatistices

class ElectionStatisticesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionStatistices
        fields = [
            'id',
            'election',
            'user',
            'time'
        ]
        write_only_fields = ['user']
        read_only_fields = ['id','time']