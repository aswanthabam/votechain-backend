from rest_framework import serializers
from db.models import State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'