from rest_framework import serializers
from db.models import SystemConfig

class SystemConfigSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.votechainAddress = validated_data.get('votechainAddress', instance.votechainAddress)
        instance.candidateAddress = validated_data.get('candidateAddress', instance.candidateAddress)
        instance.permissionsAddress = validated_data.get('permissionsAddress', instance.permissionsAddress)
        instance.voterAddress = validated_data.get('voterAddress', instance.voterAddress)
        instance.rpcUrl = validated_data.get('rpcUrl', instance.rpcUrl)
        instance.wsUrl = validated_data.get('wsUrl', instance.wsUrl)
        instance.voterReaderAddress = validated_data.get('voterReaderAddress', instance.voterReaderAddress)
        instance.linkerAddress = validated_data.get('linkerAddress', instance.linkerAddress)
        instance.localServer = validated_data.get('localServer', instance.localServer)
        instance.funderAccount = validated_data.get('funderAccount', instance.funderAccount)
        instance.save()
        return instance
    class Meta:
        model = SystemConfig
        fields = '__all__'
