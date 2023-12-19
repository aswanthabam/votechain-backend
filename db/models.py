from django.db import models
from uuid import uuid4

class SystemConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    voterAddress = models.CharField(max_length=100)
    electionAddress = models.CharField(max_length=100)
    candidateAddress = models.CharField(max_length=100)
    adminAddress = models.CharField(max_length=100)
    ipAddress = models.CharField(max_length=100)
    port = models.IntegerField()

