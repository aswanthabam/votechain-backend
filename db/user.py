from django.db import models
from uuid import uuid4

class UserAuth(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    uid = models.CharField(max_length=100, unique=True, null=False, blank=False)
    aadhar = models.CharField(max_length=100, unique=True, null=False, blank=False)
    enc1 = models.CharField(max_length=200, null=False, blank=False) # encrypted mneumonics with password
    enc2 = models.CharField(max_length=200, null=False, blank=False) # encrypted mneumonic with otp

class UserRecovery(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    userAuth = models.ForeignKey('UserAuth', on_delete=models.CASCADE, related_name='userAuth')

class UserDataAccess(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    token = models.CharField(max_length=100, unique=True, null=False, blank=False)
    scope = models.CharField(max_length=200, null=False, blank=False)