from django.db import models
from uuid import uuid4
import random, string

def random_hex():
    return '0x'+(''.join([random.choice(string.ascii_letters) for x in range(46)]))

class UserFace(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    registered = models.BooleanField(default=False)
    face = models.CharField(max_length=100, unique=True, null=True, blank=True)
    face_key = models.CharField(max_length=100,null=True,blank=True, default=random_hex)
    updated_on = models.DateTimeField(auto_now=True)

class UserAuth(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    uid = models.CharField(max_length=100, unique=True, null=False, blank=False)
    aadhar = models.CharField(max_length=100, unique=True, null=False, blank=False)
    enc1 = models.CharField(max_length=200, null=False, blank=False) # encrypted mneumonics with password
    enc2 = models.CharField(max_length=200, null=False, blank=False) # encrypted mneumonic with otp
    face = models.ForeignKey('UserFace', on_delete=models.CASCADE, related_name='user_id', null=False, blank=False)
    app_key = models.CharField(max_length=100,null=True,blank=True,unique=True)
    face_registerd = models.BooleanField(default=False)

class UserFaceCache(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    face_id = models.OneToOneField('UserFace', on_delete=models.CASCADE, related_name='face_id')
    embeddings = models.TextField(null=False, blank=False)
    embedding = models.TextField(null=False, blank=False)

    
class UserRecovery(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    userAuth = models.ForeignKey('UserAuth', on_delete=models.CASCADE, related_name='userAuth')

class UserDataAccess(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True,default=uuid4)
    token = models.CharField(max_length=100, unique=True, null=False, blank=False)
    scope = models.CharField(max_length=200, null=False, blank=False)


class AppInstance(models.Model):
    id = models.CharField(max_length=48, primary_key=True, unique=True,default=uuid4)
    userId = models.OneToOneField('UserAuth', on_delete=models.CASCADE, related_name='app_instance_user_id')
    created_at = models.DateTimeField(auto_now_add=True)

class AccessKey(models.Model):
    id = models.CharField(max_length=48, primary_key=True, unique=True,default=uuid4)
    userId = models.OneToOneField('UserAuth', on_delete=models.CASCADE, related_name='access_key_user_id')
    key = models.CharField(max_length=100, unique=True, null=False, blank=False)
    scope = models.CharField(max_length=200, null=False, blank=False)
    clientId = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
