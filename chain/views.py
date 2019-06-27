from django.shortcuts import render

# Create your views here.

def block_list(request, template_name='block_list.html'):
    return render(request, template_name)