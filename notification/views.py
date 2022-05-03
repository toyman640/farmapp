from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required 

from notification.models import Notification

# Create your views here.

@login_required(login_url='/admin-page/login')
def show_note(request, slug):
    n = Notification.objects.get(slug=slug)
    return render(request,'message-view-note.html', {'note' : n})


@login_required(login_url='/admin-page/login')
def show_noteHR(request, slug):
    n = Notification.objects.get(slug=slug)
    return render(request,'hr/message-view-notehr.html', {'note' : n})



@login_required(login_url='/admin-page/login')
def delete_note(request, note_id ):
    n = Notification.objects.get(id=note_id)
    n.viewed = True
    n.save()

    return HttpResponseRedirect('/pages/')

@login_required(login_url='/admin-page/login')
def delete_notehr(request, note_id ):
    n = Notification.objects.get(id=note_id)
    n.viewed = True
    n.save()

    return HttpResponseRedirect('/human-resources/HR-section')




