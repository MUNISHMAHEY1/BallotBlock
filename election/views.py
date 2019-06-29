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
        if request.method == 'POST':
            for p in positions:
                pname = 'position{}'.format(p.id)
                request.POST.get(pname,"")
                
        
        context['positions'] = positions
        context['quantity_of_positions'] = positions.count()
        
    else:
        messages.warning(request, 'Election is not open yet.')
    
    return render(request, 'vote.html', context)

@transaction.atomic
@staff_member_required
def config_mock_election(request, elector_quantity=500, template_name='mock_election.html'):

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

    position = Position.objects.create(description="Best city to live in Canada")
    position.save()

    names = ['Toronto', 'Vancouver', 'Windsor', 'Montreal', 'Quebec', 'Ottawa']
    for name in names:
        c = Candidate.objects.create(position=position, name=name)
        c.save()
    
    
    i = 1
    s = len(str(elector_quantity))
    while i < elector_quantity:
        username = ''.join(('user', str(i).zfill(s)))
        email = ''.join((username, '@balletblock.com'))
        password = ''.join(('BalletBlock', str(i).zfill(s) ))
        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 first_name='user',
                                 last_name=str(i).zfill(s))
        user.save()
        e = Elector.objects.create(user=user)
        e.save()
        i = i + 1

    return render(request, template_name)