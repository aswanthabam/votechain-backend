from django.db import models
from uuid import uuid4

def get_independent_party():
    party = Party.objects.filter(name='Independent').first()
    if party is not None:return party
    party = Party.objects.create(name="Independent",logo='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png')
    return party

class Party(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    name = models.CharField(max_length=200, null=False, blank=False)
    logo = models.CharField(max_length=200, null=True, blank=False,default="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png")

class CandidateProfile(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    userId = models.OneToOneField('UserAuth', on_delete=models.CASCADE, related_name='candidate_profile_user', null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    candidateAddress = models.CharField(max_length=100,null=False, blank=False, unique=True,default=uuid4)
    photo = models.CharField(max_length=200, null=True, blank=False,default="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png")
    about = models.TextField(null=True, blank=False)
    phone = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    address = models.TextField(max_length=200, null=True, blank=False)
    party = models.ForeignKey('Party', on_delete=models.CASCADE, related_name='candidate_profile_party', null=True, blank=False, default=get_independent_party)
    logo = models.CharField(max_length=200, null=True, blank=False)

class CandidateDocumentLinker(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    candidate = models.ForeignKey('CandidateProfile', on_delete=models.CASCADE, related_name='candidate_document_candidate', null=False, blank=False)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='candidate_document_document', null=False, blank=False)
    
class Document(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    title = models.CharField(max_length=200, null=False, blank=False)
    link = models.CharField(max_length=200, null=False, blank=False)

class Education(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True, default=uuid4)
    title = models.CharField(max_length=200, null=False, blank=False)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education_candidate', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    fromWhere = models.CharField(max_length=200, null=True, blank=False)

class Experience(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    title = models.CharField(max_length=200, null=False, blank=False)
    candidate = models.ForeignKey('CandidateProfile', on_delete=models.CASCADE, related_name='work_experience_candidate', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    fromWhere = models.CharField(max_length=200, null=True, blank=False)

