from django.db import models
from uuid import uuid4

class ElectionStatistices(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null=False,blank=False, unique=True,default=uuid4)
    user = models.ForeignKey('UserAuth', on_delete=models.CASCADE, related_name='election_user', null=False, blank=False)
    election = models.IntegerField(null=False, blank=False)
    time = models.DateTimeField(null=False, blank=False, auto_now=True)