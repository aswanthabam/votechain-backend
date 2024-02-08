from rest_framework import serializers
from db.user import UserAuth,UserFace, random_hex
from utils.encryption import encrypt
class UserAuthSerializer(serializers.ModelSerializer):
    face_id = serializers.CharField(read_only=True, source='face.id')
    app_key = serializers.SerializerMethodField()
    
    def create(self, validated_data):
        face = UserFace.objects.create()
        app_key = random_hex()
        app_key = random_hex()
        obj =  UserAuth(**{
            'uid': validated_data['uid'],
            'aadhar': validated_data['aadhar'],
            'enc1': validated_data['enc1'],
            'enc2': validated_data['enc2'],
            'face': face,
            'app_key': app_key
        })
        obj.save()
        return obj
    
    def get_app_key(self, obj):
        return encrypt(obj.app_key, obj.face.face_key)
    
    class Meta:
        model = UserAuth
        fields = [
            'uid',
            'aadhar',
            'enc1',
            'enc2',
            'face_id',
            'app_key'
        ]
        write_only_fields = ['id','uid','aadhar']