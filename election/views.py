from django.shortcuts import render
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

# def electionConfiguration(request):
#     form = ElectionConfigForm()
#     queryset = ElectionConfig.objects.get(id = 1)
#     if request.POST:
#         form = ElectionConfigForm(request.POST,instance=queryset)
#         locked = request.POST.get('locked')
#         start_time = request.POST.get('start_time')
#         end_time = request.POST.get('end_time')
#
#         if locked:
#             if form.is_valid():
#                 if start_time > datetime.now():
#                     if end_time > datetime.now():
#                         if start_time < end_time:
#                             form.save()
#                             form = ElectionConfigForm()
#                             msg = 'The Configuration for upcomming election has been set. Start time of election is {td1} and End time is {td2}'.format(td1=start_time, td2= end_time)
#                             messages.success(request, msg)
#                             return render(request,'electionconfig.html',{'form':form})
#                         else:
#                             msg = 'End time {td1} cannot be less then start time {td2}.'.format(td2=start_time, td1= end_time)
#                             messages.error(request, msg)
#                     else:
#                         msg = 'End time {td1} cannot be in the past.'.format(td1= end_time)
#                         messages.error(request, msg)
#                 else:
#                     msg = 'Start time {td1} cannot be in the past.'.format(td1= start_time)
#                     messages.error(request, msg)
#             else:
#                 msg = 'The form filled is not valid please check if all the fields are entered properly.'
#                 messages.warning(request, msg)
#         else:
#             msg = 'After filling up the configurations please check if the election is locked.'
#             messages.warning(request,msg)
#     form = ElectionConfigForm()
#     return render(request,'electionconfig.html',{'form':form})

def electionConfiguration(request):
    form = ElectionConfigForm()
    queryset = ElectionConfig.objects.get(id = 1)
    if request.POST:
        form = ElectionConfigForm(request.POST,instance=queryset)
        locked = request.POST.get('locked')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        print("\nStart time =",start_time)
        # end_time_modle = ElectionConfig.end_time

        if locked:
            if form.is_valid():
                form.save()
                form = ElectionConfigForm()
                msg = 'The Configuration for upcomming election has been set. Start time of election is {td1} and End time is {td2}'.format(td1=start_time, td2= end_time)
                messages.success(request, msg)
                return render(request,'electionconfig.html',{'form':form})
            else:
                msg = 'The form filled is not valid please check if all the fields are entered properly. Specially check for the start time and end time.'
                messages.error(request, msg)
        else:
            msg = 'After filling up the configurations please check if the election is locked.'
            messages.warning(request,msg)
    form = ElectionConfigForm()
    return render(request,'electionconfig.html',{'form':form})


def electionConfigurationViewOnly(request):
    form = electionconfigviewForm()
    return render(request,'electionconfigview.html',{'form':form})
