from django.db import models

# Create your models here.

#Decided that another db is not required because the hash for the databases and the source code is generated each time anyway.
class BlockStructure(models.Model):
     BlockNo= models.IntegerField(unique=True,null=False,blank=False)
     ParentHash=models.CharField(max_length=200, null=True, blank=False, default=None)

class BBlock(models.Model):
     block_no=models.IntegerField(unique=True,null=False, blank=False)
     db_hash=models.TextField(blank=False,unique=True)
     sc_hash=models.TextField(blank=False,unique=True)
     candidate_votes=models.TextField(blank=True,null=True)
     candidate_votes=models.TextField(blank=True,null=True)
     voters_voted=models.TextField(blank=True,null=True)
     total_votes=models.IntegerField(blank=False)
     parent_hash=models.TextField(blank=False,unique=True)
     