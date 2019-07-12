from django.db import models

# Create your models here.

#Decided that another db is not required because the hash for the databases and the source code is generated each time anyway.
class BlockStructure(models.Model):
     BlockNo= models.IntegerField(unique=True,null=False,blank=False)
     ParentHash=models.CharField(max_length=200, null=True, blank=False, default=None)

class BBlock_db(models.Model):
     block_no=models.IntegerField(unique=True,null=False, blank=False)
     block_hash = models.CharField(max_length=2048, null=False, blank=False)
     previous_hash = models.CharField(max_length=2048, null=False, blank=False)
     database_hash=models.TextField(blank=False,unique=True)
     source_code_hash=models.TextField(blank=False,unique=True)
     candidate_votes=models.TextField(blank=True,null=True)
     electors=models.TextField(blank=True,null=True)
     timestamp_iso = models.CharField(max_length=30, null=False, blank=False)
     total_votes=models.IntegerField(blank=False)
     parent_hash=models.TextField(blank=False,unique=True)
     