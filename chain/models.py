from django.db import models

# Create your models here.

#Decided that another db is not required because the hash for the databases and the source code is generated each time anyway.
class BlockStructure(models.Model):
     BlockNo= models.IntegerField(unique=True,null=False,blank=False)
     ParentHash=models.CharField(max_length=200, null=True, blank=False, default=None)