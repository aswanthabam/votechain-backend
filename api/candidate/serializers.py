from rest_framework import serializers
from db.user import UserAuth
from db.candidate import CandidateProfile, Education, Experience
from rest_framework.exceptions import ValidationError

class CandidateProfileSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        obj =  CandidateProfile(**{
            'candidateId': validated_data['candidateId'],
            'about': validated_data['about'],
            'photo': validated_data['photo']
        })
        obj.save()
        return obj
    class Meta:
        model = CandidateProfile
        fields = [
            'candidateId',
            'about',
            'photo',
        ]

class CandidateEducationSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        candidate = CandidateProfile.objects.filter(candidateId=validated_data['candidateId']).first()
        if candidate is None:
            raise ValidationError("Candidate does not exist.")
        obj =  Education(**{
            'title': validated_data['title'],
            'description': validated_data['description'],
            'fromWhere': validated_data['fromWhere'],
            'candidate': candidate
        })
        obj.save()
        return obj
    class Meta:
        model = Education
        fields = [
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]

class CandidateExperienceSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        candidate = CandidateProfile.objects.filter(candidateId=validated_data['candidateId']).first()
        if candidate is None:
            raise ValidationError("Candidate does not exist.")
        obj =  Experience(**{
            'title': validated_data['title'],
            'description': validated_data['description'],
            'fromWhere': validated_data['fromWhere'],
            'candidate': candidate
        })
        obj.save()
        return obj
    class Meta:
        model = Experience
        fields = [
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]

class CandidateProfileSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        obj =  CandidateProfile(**{
            'candidateId': validated_data['candidateId'],
            'about': validated_data['about'],
            'photo': validated_data['photo']
        })
        obj.save()
        return obj
    class Meta:
        model = CandidateProfile
        fields = [
            'candidateId',
            'about',
            'photo',
        ]

class CandidateEducationSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        candidate = CandidateProfile.objects.filter(candidateId=validated_data['candidateId']).first()
        if candidate is None:
            
        obj =  Education(**{
            'title': validated_data['title'],
            'description': validated_data['description'],
            'fromWhere': validated_data['fromWhere'],
            'candidate': candidate
        })
        obj.save()
        return obj
    class Meta:
        model = Education
        fields = [
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]

class CandidateExperienceSerializer(serializers.ModelSerializer):
    candidateId = serializers.IntegerField()
    def create(self, validated_data):
        candidate = CandidateProfile.objects.filter(candidateId=validated_data['candidateId']).first()
        if candidate is None:
            return None
        obj =  Experience(**{
            'title': validated_data['title'],
            'description': validated_data['description'],
            'fromWhere': validated_data['fromWhere'],
            'candidate': candidate
        })
        obj.save()
        return obj
    class Meta:
        model = Experience
        fields = [
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]