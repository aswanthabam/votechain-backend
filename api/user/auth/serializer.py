from rest_framework import serializers
from db.user import UserAuth

class UserAuthSerializer(serializers.ModelSerializer):
    face_id = serializers.CharField(read_only=True, source='face.id')
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
        fields = [
            'uid',
            'aadhar',
            'enc1',
            'enc2',
            'face_id'
        ]
        write_only_fields = ['id','uid','aadhar']