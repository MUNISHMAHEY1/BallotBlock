from django.shortcuts import render, redirect
from election.models import Elector, Candidate, ElectionConfig, Position
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from datetime import datetime
from election.business import ElectionBusiness
from django.contrib import messages
from election.forms import VoteForm,ElectionConfigForm, CandidateForm, PositionForm, ElectorForm
from election.signals import canModify
from election.middleware import ElectionMiddleware
from election.tables import CandidateTable, PositionTable, ElectorTable
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

     # Create 3rd position
    position = Position.objects.create(description="Best programming language")
    position.save()

    names = ['Python', 'Javascript', 'Java', 'C#', 'PHP', 'Prolog']
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

# Only staff members can access the election configuration
@staff_member_required
def electionConfiguration(request, template_name='electionconfig.html'):

    ec = None
    # If exists at least one row in the table
    if ElectionConfig.objects.all().count() > 0:
        # Select all rows and get the first one.
        ec = ElectionConfig.objects.filter()[0]

    if request.election_is_occurring:
        form = ElectionConfigForm(instance=ec, readonly=request.election_is_occurring)
        return render(request, template_name, {'form':form})

    if request.POST:
        form = ElectionConfigForm(request.POST, instance=ec, readonly=request.election_is_occurring)
        if form.is_valid():
            form.save()
            msg = 'Election configuration saved'
            messages.success(request, msg)
            return redirect('electionconfig')
        return render(request, template_name, {'form':form})
    else:
        form = ElectionConfigForm(instance=ec)

    return render(request, template_name, {'form':form})

@staff_member_required
def candidate(request, template_name='candidate/candidate_list.html'):
    candidate_table = CandidateTable(Candidate.objects.all())
    # Exclude delete column if election is occurring
    if request.election_is_occurring:
        candidate_table.exclude = ('delete')
    return render(request, template_name, {'candidate_table':candidate_table })

@staff_member_required
def candidate_delete(request, id):
    if request.election_is_occurring:
        msg = 'Election is occurring. Delete candidates is not allowed.'
        messages.error(request, msg)
        return redirect('candidate')

    try:
        Candidate.objects.get(id=int(id)).delete()
    except Exception as e:
        s = str(e)
        messages.error(request, e)

    return redirect('candidate')

@staff_member_required
def candidate_add(request, template_name='candidate/candidate_form.html'):
    if request.election_is_occurring:
        msg = 'Election is occurring. Candidate modifications are not allowed.'
        messages.warning(request, msg)
        return redirect('candidate')

    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidate')
        else:
            return render(request, template_name, {'form':form})
    else:
        form = CandidateForm()
    return render(request, template_name, {'form':form})

@staff_member_required
def candidate_change(request, id, template_name='candidate/candidate_form.html'):
    candidate = Candidate.objects.get(id=int(id))
    if request.POST:
        if request.election_is_occurring:
            msg = 'Election is occurring. Candidate modifications are not allowed.'
            messages.error(request, msg)
            return redirect('candidate')

        form = CandidateForm(request.POST, instance=candidate, readonly=request.election_is_occurring)
        if form.is_valid():
            form.save()
            return redirect('candidate')
        else:
            return render(request, template_name, {'form':form})
    else:
        # If election is occurring, the form will be readonly
        form = CandidateForm(instance=candidate, readonly=request.election_is_occurring)
    return render(request, template_name, {'form':form})

@staff_member_required
def position(request, template_name='position/position_list.html'):
    position_table = PositionTable(Position.objects.all())
    # Exclude delete column if election is occurring
    if request.election_is_occurring:
        position_table.exclude = ('delete')
    return render(request, template_name, {'position_table':position_table })

@staff_member_required
def position_delete(request, id):
    if request.election_is_occurring:
        msg = 'Election is occurring. Delete position is not allowed.'
        messages.error(request, msg)
        return redirect('position')

    try:
        Position.objects.get(id=int(id)).delete()
    except Exception as e:
        s = str(e)
        messages.error(request, e)

    return redirect('position')

@staff_member_required
def position_add(request, template_name='position/position_form.html'):
    if request.election_is_occurring:
        msg = 'Election is occurring. Position modifications are not allowed.'
        messages.warning(request, msg)
        return redirect('position')

    if request.POST:
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position')
        else:
            return render(request, template_name, {'form':form})
    else:
        form = PositionForm()
    return render(request, template_name, {'form':form})

@staff_member_required
def position_change(request, id, template_name='position/position_form.html'):
    position = Position.objects.get(id=int(id))
    if request.POST:
        if request.election_is_occurring:
            msg = 'Election is occurring. Position modifications are not allowed.'
            messages.error(request, msg)
            return redirect('position')

        form = PositionForm(request.POST, instance=position, readonly=request.election_is_occurring)
        if form.is_valid():
            form.save()
            return redirect('position')
        else:
            return render(request, template_name, {'form':form})
    else:
        # If election is occurring, the form will be readonly
        form = PositionForm(instance=position, readonly=request.election_is_occurring)
    return render(request, template_name, {'form':form})




@staff_member_required
def elector(request, template_name='elector/elector_list.html'):
    elector_table = ElectorTable(Elector.objects.all())
    # Exclude delete column if election is occurring
    if request.election_is_occurring:
        elector_table.exclude = ('delete')
    return render(request, template_name, {'elector_table':elector_table })

@staff_member_required
def elector_delete(request, id):
    if request.election_is_occurring:
        msg = 'Election is occurring. Delete electors is not allowed.'
        messages.error(request, msg)
        return redirect('elector')

    try:
        Elector.objects.get(id=int(id)).delete()
    except Exception as e:
        s = str(e)
        messages.error(request, e)

    return redirect('elector')

@staff_member_required
def elector_add(request, template_name='elector/elector_form.html'):
    if request.election_is_occurring:
        msg = 'Election is occurring. Elector modifications are not allowed.'
        messages.warning(request, msg)
        return redirect('elector')

    if request.POST:
        form = ElectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('elector')
        else:
            return render(request, template_name, {'form':form})
    else:
        form = ElectorForm()
    return render(request, template_name, {'form':form})

@staff_member_required
def elector_change(request, id, template_name='elector/elector_form.html'):
    elector = Elector.objects.get(id=int(id))
    if request.POST:
        if request.election_is_occurring:
            msg = 'Election is occurring. Elector modifications are not allowed.'
            messages.error(request, msg)
            return redirect('elector')

        form = ElectorForm(request.POST, instance=elector, readonly=request.election_is_occurring)
        if form.is_valid():
            form.save()
            return redirect('elector')
        else:
            return render(request, template_name, {'form':form})
    else:
        # If election is occurring, the form will be readonly
        form = ElectorForm(instance=elector, readonly=request.election_is_occurring)
    return render(request, template_name, {'form':form})
