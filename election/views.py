from django.shortcuts import render
from election.models import Elector, Candidate, ElectionConfig, Position
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from election.business import ElectionBusiness
from django.contrib import messages
from election.forms import VoteForm

# Create your views here.

def vote(request):
    eb = ElectionBusiness()
    context = {}
    if eb.isOccurring():
        positions = Position.objects.all()
        context['postitions'] = positions
    else:
        messages.warning(request, 'Election is not open yet.')
    
    return render(request, 'vote.html', context)

@transaction.atomic
@staff_member_required
def config_mock_election(request, elector_quantity=1000, template_name='mock_election.html'):

    Elector.objects.all().delete()
    Candidate.objects.all().delete()
    Position.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    position = Position.objects.create(description="Best soccer player of all time")
    position.save()

    names = ['Pele', 'Messi', 'Cristiano Ronaldo', 'Zidane', 'Ronaldo', 'Romario']
    for name in names:
        c = Candidate.objects.create(position=position, name=name)
        c.save()
    
    i = 1
    while i < elector_quantity:
        username = ''.join(('user', str(i).zfill(4)))
        email = ''.join((username, '@balletblock.com'))
        password = ''.join(('BalletBlock', str(i).zfill(4))) 
        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 first_name='user',
                                 last_name=str(i).zfill(4))
        user.save()
        e = Elector.objects.create(user=user)
        e.save()
        i = i + 1

    return render(request, template_name)