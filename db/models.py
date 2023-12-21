from django.db import models
from uuid import uuid4

class SystemConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    voterAddress = models.CharField(max_length=100)
    # electionAddress = models.CharField(max_length=100)
    candidateAddress = models.CharField(max_length=100)
    permissionsAddress = models.CharField(max_length=100)
    votechainAddress = models.CharField(max_length=100)
    voterReaderAddress = models.CharField(max_length=100)
    linkerAddress = models.CharField(max_length=100)
    # adminAddress = models.CharField(max_length=100)
    rpcUrl = models.CharField(max_length=100)
    wsUrl = models.CharField(max_length=100)

class State(models.Model):
    id = models.CharField(default=uuid4,max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)

class District(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid4)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, related_name='state')

class Constituency(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True, default=uuid4)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE, related_name='district')
