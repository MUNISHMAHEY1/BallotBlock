from django.shortcuts import render
from chain.business import BBlock
# Create your views here.

def block_list(request, template_name='block_list.html'):
    BBlock.write(1)
    return render(request, template_name)
