from rest_framework import serializers
from db.user import UserAuth
from db.candidate import CandidateProfile, Education, Experience, CandidateDocumentLinker
from rest_framework.validators import UniqueValidator

class CandidateProfileSerializer(serializers.ModelSerializer):
    
    candidateId = serializers.IntegerField(validators=[UniqueValidator(queryset=CandidateProfile.objects.all(),message='Candidate already has a profile')])
    profileId = serializers.CharField(read_only=True, source='id')
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    def create(self, validated_data):
        obj =  CandidateProfile(**{
            'candidateId': validated_data['candidateId'],
            'about': validated_data['about'],
            'photo': validated_data['photo'],
            'userId': validated_data['userId']
        })
        obj.save()
        return obj
    
    def get_education(self, obj):
        education = Education.objects.filter(candidate=obj).all()
        return CandidateEducationSerializer(education, many=True).data
    
    def get_experience(self, obj):
        experience = Experience.objects.filter(candidate=obj).all()
        return CandidateExperienceSerializer(experience, many=True).data
    
    def get_documents(self, obj):
        documents = CandidateDocumentLinker.objects.filter(candidate=obj).all()
        return [{
            'title':x.document.title,
            'link':x.document.link
        } for x in documents]
    
    class Meta:
        model = CandidateProfile
        fields = [
            'profileId',
            'candidateId',
            'about',
            'photo',
            'education',
            'experience',
            'documents',
            'userId'
        ]

class CandidateEducationSerializer(serializers.ModelSerializer):

    candidateId = serializers.IntegerField(source='candidate.candidateId')
    educationId = serializers.CharField(read_only=True, source='id')

    def validate_candidateId(self, attrs):
        print(attrs)
        candidate = CandidateProfile.objects.filter(candidateId=attrs).first()
        if candidate is None:
            raise serializers.ValidationError("Candidate does not exist.")
        return candidate
    
    def create(self, validated_data):
        print(validated_data)
        obj =  Education(**{
            'title': validated_data.get('title'),
            'description': validated_data.get('description'),
            'fromWhere': validated_data.get('fromWhere'),
            'candidate': validated_data.get('candidate').get('candidateId')
        })
        obj.save()
        return obj
    class Meta:
        model = Education
        fields = [
            'educationId',
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]
class CandidateExperienceSerializer(serializers.ModelSerializer):

    candidateId = serializers.IntegerField(source='candidate.candidateId')
    experienceId = serializers.CharField(read_only=True, source='id')

    def validate_candidateId(self, attrs):
        print(attrs)
        candidate = CandidateProfile.objects.filter(candidateId=attrs).first()
        if candidate is None:
            raise serializers.ValidationError("Candidate does not exist.")
        return candidate
    
    def create(self, validated_data):
        print(validated_data)
        obj =  Experience(**{
            'title': validated_data.get('title'),
            'description': validated_data.get('description'),
            'fromWhere': validated_data.get('fromWhere'),
            'candidate': validated_data.get('candidate').get('candidateId')
        })
        obj.save()
        return obj
    class Meta:
        model = Experience
        fields = [
            'experienceId',
            'title',
            'description',
            'fromWhere',
            'candidateId'
        ]
