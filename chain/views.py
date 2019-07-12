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