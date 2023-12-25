from rest_framework import serializers
from db.user import UserAuth
from utils.encryption import encrypt
from django.conf import settings

class UserAuthSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        obj =  UserAuth(**{
            'uid': validated_data['uid'],
            'aadhar': validated_data['aadhar'],
            'enc1': validated_data['enc1'],
            'enc2': validated_data['enc2']
        })
        obj.save()
        return obj
    
    class Meta:
        model = UserAuth
        fields = '__all__'
        write_only_fields = ['id','uid','aadhar']