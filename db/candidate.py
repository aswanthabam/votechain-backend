from django.db import models

class CandidateProfile(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True)
    candidateId = models.IntegerField(max_length=100,null=False, blank=False)
    photo = models.CharField(max_length=200, null=True, blank=False)
    about = models.TextField(null=True, blank=False)

class CandidateDocumentLinker(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True)
    candidate = models.ForeignKey('CandidateProfile', on_delete=models.CASCADE, related_name='candidate_document_candidate', null=False, blank=False)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='candidate_document_document', null=False, blank=False)
    
class Document(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    link = models.CharField(max_length=200, null=False, blank=False)

class Education(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    candidate = models.ForeignKey('CandidateProfile', on_delete=models.CASCADE, related_name='education_candidate', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    fromWhere = models.CharField(max_length=200, null=True, blank=False)

class Experience(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    candidate = models.ForeignKey('CandidateProfile', on_delete=models.CASCADE, related_name='work_experience_candidate', null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    fromWhere = models.CharField(max_length=200, null=True, blank=False)