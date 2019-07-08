from django.db import models
from election.models import Elector, Candidate

class Voted(models.Model):
    elector = models.OneToOneField(Elector, blank=False, null=False, unique=True, on_delete=models.PROTECT)
    hash_val= models.CharField(max_length=200, null=True, blank=False, default=None)

class CandidateVote(models.Model):
    candidate = models.OneToOneField(Candidate, blank=False, null=False, unique=True, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False, blank=False, default=0)
