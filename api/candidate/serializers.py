from rest_framework import serializers
from db.candidate import CandidateProfile, Education, Experience, CandidateDocumentLinker, get_independent_party
from rest_framework.validators import UniqueValidator

class CandidateProfileSerializer(serializers.ModelSerializer):
    
    candidateAddress = serializers.CharField(validators=[UniqueValidator(queryset=CandidateProfile.objects.all(),message='Candidate with address already has a profile')])
    profileId = serializers.CharField(read_only=True, source='id')
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    # partyId = serializers.CharField(source='party.id')
    candidate_party = serializers.SerializerMethodField()

    def create(self, validated_data):
        obj =  CandidateProfile(**{
            'candidateAddress': validated_data.get('candidateAddress'),
            'about': validated_data.get('about'),
            'photo': validated_data.get('photo'),
            'userId': validated_data.get('userId'),
            'name': validated_data.get('name'),
            'phone':validated_data.get('phone'),
            'email':validated_data.get('email'),
            'address':validated_data.get('address'),
            'party':get_independent_party() if validated_data.get('party') is None else validated_data.get('party'),
            'logo':validated_data.get('logo'),
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
    
    def get_candidate_party(self, obj):
        return {
            'partyId':obj.party.id,
            'name':obj.party.name,
            'logo':obj.party.logo
        }
    class Meta:
        model = CandidateProfile
        fields = [
            'profileId',
            'candidateAddress',
            'about',
            'photo',
            'education',
            'experience',
            'documents',
            'name',
            'userId',
            'phone',
            'email',
            'address',
            'party',
            'logo',
            'candidate_party'
        ]

class CandidateEducationSerializer(serializers.ModelSerializer):

    educationId = serializers.CharField(read_only=True, source='id')
    
    def create(self, validated_data):
        print(validated_data)
        obj =  Education(**{
            'title': validated_data.get('title'),
            'description': validated_data.get('description'),
            'fromWhere': validated_data.get('fromWhere'),
            'candidate': self.context.get('candidate')
        })
        obj.save()
        return obj
    class Meta:
        model = Education
        fields = [
            'educationId',
            'title',
            'description',
            'fromWhere'
        ]
class CandidateExperienceSerializer(serializers.ModelSerializer):

    experienceId = serializers.CharField(read_only=True, source='id')
    
    def create(self, validated_data):
        print(validated_data)
        obj =  Experience(**{
            'title': validated_data.get('title'),
            'description': validated_data.get('description'),
            'fromWhere': validated_data.get('fromWhere'),
            'candidate': self.context.get('candidate')
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
        ]
