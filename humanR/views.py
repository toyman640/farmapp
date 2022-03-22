from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from humanR.models import *
from farmrecord.forms import WorkerForm
from django.contrib import messages

# Create your views here.

@login_required(login_url='/admin-page/login')
def index(request):
    return render(request, 'hr/index.html')

@login_required(login_url='/admin-page/login')
def new_entry(request):
    if request.method == 'POST':
        new_worker = WorkerForm(request.POST, request.FILES)
        if new_worker.is_valid():
            new_worker.save()
            messages.success(request, 'Entry Saved')
            new_worker = WorkerForm()
    else:
        new_worker = WorkerForm()
    return render(request, 'hr/new-entry.html', {'employ' : new_worker})