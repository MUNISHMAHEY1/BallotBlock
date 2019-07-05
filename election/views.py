from django.shortcuts import render, redirect
from election.models import Elector, Candidate, ElectionConfig, Position
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from datetime import datetime
from election.business import ElectionBusiness
from django.contrib import messages
from election.forms import VoteForm,ElectionConfigForm, electionconfigviewForm
from election.signals import canModify
from election.middleware import ElectionMiddleware
from election.tables import CandidateTable
from django_tables2.config import RequestConfig

@transaction.atomic
@staff_member_required
def config_mock_election(request, elector_quantity=500, template_name='mock_election.html'):

    # Clean database
    Elector.objects.all().delete()
    Candidate.objects.all().delete()
    Position.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    # Create 1st position
    position = Position.objects.create(description="Best soccer player of all time")
    position.save()

    names = ['Pele', 'Messi', 'Cristiano Ronaldo', 'Zidane', 'Ronaldo', 'Romario']
    for name in names:
        c = Candidate.objects.create(position=position, name=name)
        c.save()

    # Create 2nd position
    position = Position.objects.create(description="Best city to live in Canada")
    position.save()

    names = ['Toronto', 'Vancouver', 'Windsor', 'Montreal', 'Quebec', 'Ottawa']
    for name in names:
        c = Candidate.objects.create(position=position, name=name)
        c.save()


    # Create "elector_quantity" of electors
    # username: userXXX
    # pass: BalletBlockXXX
    # where XXX is ther user number from 001 to elector_quantity

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


def electionConfiguration(request, template_name='electionconfig.html'):

    if request.election_is_occurring:
        form = electionconfigviewForm()
        return render(request, template_name, {'form':form})

    ec = None
    # If exists at least one row in the table
    if ElectionConfig.objects.all().count() > 0:
        # Select all rows and get the first one.
        ec = ElectionConfig.objects.filter()[0]
    
    if request.POST:
        form = ElectionConfigForm(request.POST, instance=ec)
        if form.is_valid():
            form.save()
            msg = 'Election configuration saved'
            messages.success(request, msg)
            return redirect('electionconfig')
        return render(request, template_name, {'form':form})
    else:
        form = ElectionConfigForm(instance=ec)
    
    return render(request, template_name, {'form':form})
    
def candidate(request, template_name='candidate/candidate_list.html'):
    candidate_table = CandidateTable(Candidate.objects.all())
    #RequestConfig(request, paginate={'per_page': 5}).configure(candidate_table)
    return render(request, template_name, {'candidate_table':candidate_table })

def candidate_add(request, template_name='candidate/candidate_form.html'):
    pass

def candidate_change(request, id, template_name='candidate/candidate_form.html'):
    pass