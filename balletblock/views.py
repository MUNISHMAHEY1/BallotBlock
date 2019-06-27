from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db.models import Count, F
from django.utils import timezone
from django.http import JsonResponse
from django.forms import formset_factory, inlineformset_factory
import datetime
from django.db import transaction
from django_tables2 import RequestConfig


@login_required
def home(request):
	if request.user.is_superuser:
		return render(request, 'home.html')
	else:
		return render(request, 'vote.html')

@login_required
def about_us(request):
	return render(request, 'about_us.html')

def hash_test(request):
	
	import hashlib
	import os

	# BUF_SIZE is totally arbitrary, change for your app!
	BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

	md5 = hashlib.md5()
	sha1 = hashlib.sha1()
	
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'models.py')

	with open(file_path, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			md5.update(data)
			sha1.update(data)

	print("MD5: {0}".format(md5.hexdigest()))
	print("SHA1: {0}".format(sha1.hexdigest()))

	return HttpResponse("SHA1: {0}".format(sha1.hexdigest()))
