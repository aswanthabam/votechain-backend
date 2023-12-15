from django.db import models

class SystemConfig(models.Model):
    voterAddress = models.CharField(max_length=100)
    electionAddress = models.CharField(max_length=100)
    candidateAddress = models.CharField(max_length=100)
    adminAddress = models.CharField(max_length=100)
    ipAddress = models.CharField(max_length=100)
    port = models.IntegerField()

