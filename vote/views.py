from django.shortcuts import render
from election.models import Position, Candidate, Elector
from vote.models import Voted, CandidateVote
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
import datetime
from election.business import ElectionBusiness
from django.contrib import messages


# Create your views here.

@login_required
@transaction.atomic
def vote(request, template_name='vote.html'):
    eb = ElectionBusiness()
    context = {}
    if eb.isOccurring():
        # Check if elector already voted.
        if Voted.objects.filter(elector__user=request.user).count() > 0:
            messages.warning(request, 'You have already voted.')   
            return render(request, template_name, context)

        positions = Position.objects.all()
        if request.method == 'POST':
            try:
                for p in positions:
                    pname = 'position{}'.format(p.id)
                    candidate_id = request.POST.get(pname,"")
                    candidate = Candidate.objects.get(id=int(candidate_id))
                    cv, created = CandidateVote.objects.get_or_create(candidate=candidate)
                    cv.quantity = cv.quantity + 1
                    cv.save()
                elector = Elector.objects.get(user=request.user)
                voted = Voted.objects.create(elector=elector)
                voted.save()
                messages.success(request, 'Your vote was registred successfully')
            except Exception as e:
                messages.error(request, str(e))
        else:
            context['positions'] = positions
            context['quantity_of_positions'] = positions.count()
    else:
        messages.warning(request, 'Election is not open yet.')
    
    return render(request, template_name, context)
