from rest_framework import serializers
from db.models import SystemConfig

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'
