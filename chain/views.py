from django.shortcuts import render, redirect
from chain.business import BBlockHandler
from chain.models import BBlock
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers
# Create your views here.

def block_list(request, template_name='block_list.html'):
    bblock_list = BBlock.objects.all()
    return render(request, template_name, {'bblock_list': bblock_list})

def block_add(request):
    BBlockHandler().add()
    return redirect('block_list')

def database_hash(request, bblock_id, template_name='database_hash.html'):
    bblock = BBlock.objects.get(id=int(bblock_id))
    #database_hash_dict = json.loads(bblock.database_hash, cls=DjangoJSONEncoder)
    database_hash_dict = json.loads(bblock.database_hash)
    return render(request, template_name, {'bblock': bblock, 'database_hash_dict': database_hash_dict})

def source_code_hash(request, bblock_id, template_name='source_code_hash.html'):
    bblock = BBlock.objects.get(id=int(bblock_id))
    return render(request, template_name, {'bblock': bblock})

