from rest_framework import serializers
from db.user import UserAuth
from utils.encryption import encrypt
from django.conf import settings

class UserAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,write_only=True)

    def create(self, validated_data):
        validated_data['enc2'] = encrypt(validated_data['enc2'],settings.SECRET_KEY).hex()
        validated_data['enc1'] = encrypt(validated_data['enc1'],validated_data['password']).hex()
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