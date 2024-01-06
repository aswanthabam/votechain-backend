from django.db import models
from uuid import uuid4
import os

class SystemConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    voterAddress = models.CharField(max_length=100)
    candidateAddress = models.CharField(max_length=100)
    permissionsAddress = models.CharField(max_length=100)
    votechainAddress = models.CharField(max_length=100)
    voterReaderAddress = models.CharField(max_length=100)
    linkerAddress = models.CharField(max_length=100)
    rpcUrl = models.CharField(max_length=100)
    wsUrl = models.CharField(max_length=100)
    funderAccount = models.CharField(max_length=200,default=os.environ.get('FUNDER_ACCOUNT'))
    localServer = models.CharField(max_length=200,default="http://localhost:8000")
    websocketServer = models.CharField(max_length=200,default="ws://localhost:8000")

class State(models.Model):
    id = models.CharField(primary_key=True,default=uuid4,max_length=100,null=False,blank=False, unique=True, db_column='id')
    code = models.CharField(max_length=10, unique=True,null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    no_of_districts = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        db_table = 'states'
        managed = False

class District(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True, default=uuid4, db_column='id')
    code = models.CharField(max_length=10, unique=True,null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(max_length=200, null=False, blank=False)
    no_of_constituencies = models.IntegerField(null=False, blank=False, default=0)
    link = models.TextField(null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    image = models.CharField(max_length=200, null=True, blank=False)

    class Meta:
        db_table = 'districts'
        managed = False

class Constituency(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True, default=uuid4, db_column='id')
    code = models.CharField(max_length=10, unique=True,null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    district = models.CharField(max_length=200, null=False, blank=False)
    link = models.CharField(max_length=200, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    image = models.CharField(max_length=200, null=True, blank=False)

    class Meta:
        db_table = 'constituencies'
        managed = False
