from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Poll, Vote 

# Create your views here.
def poll_page(request, item_id, thumbs_up_chosen):
    poll = get_object_or_404(RunningPoll, pk=item_id)
    user = request.user
    already_voted = Vote.objects.filter(user=user, item=item).first
    if already_voted:
        messages.error (request, 'You have already cast a vote.')

    if thumbs_up_chosen:
        item.thumbs_up_count += 1
        Poll.objects.create(user=user, item=item, thumbs_up_chosen=True)

    else:
        item.thumbs_down_count += 1
        Poll.objects.create(user=user, item=item, thumbs_down=True)

    return render(request, '', {'item':item})
    