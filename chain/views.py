from django.shortcuts import render, redirect
from chain.business import BBlockHandler
from chain.models import BBlock
# Create your views here.

def block_list(request, template_name='block_list.html'):
    bblock_list = BBlock.objects.all()
    return render(request, template_name, {'bblock_list': bblock_list })

def block_add(request):
    BBlockHandler().add()
    return redirect('block_list')

def database_hash(request, bblock_id, template_name='database_hash.html'):
    bblock = BBlock.objects.get(id=int(bblock_id))
    return render(request, template_name, {'bblock': bblock})

def source_code_hash(request, bblock_id, template_name='source_code_hash.html'):
    bblock = BBlock.objects.get(id=int(bblock_id))
    return render(request, template_name, {'bblock': bblock})

