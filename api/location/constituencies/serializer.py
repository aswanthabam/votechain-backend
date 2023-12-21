from rest_framework import serializers
from db.models import Constituency

class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'