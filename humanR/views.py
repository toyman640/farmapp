from tkinter import E
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from farmrecord.models import Section
from humanR.models import *
from farmrecord.forms import WorkerForm
from django.contrib import messages
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='/admin-page/login')
def index(request):
    worker = Employee.objects.all().count()
    section = FarmSection.objects.all().annotate(sec_count=Count('employee'))
    return render(request, 'hr/index.html', {'section': section, 'worker' : worker})

@login_required(login_url='/admin-page/login')
def new_entry(request):
    if request.method == 'POST':
        print('i started')
        new_worker = WorkerForm(request.POST, request.FILES)
        if new_worker.is_valid():
            new_worker.save()
            messages.success(request, 'Entry Saved')
            new_worker = WorkerForm()
            print('valid')
        else:
            messages.error(request, 'form not valid')
    else:
        print('not valid')
        new_worker = WorkerForm()
    return render(request, 'hr/new-entry.html', {'employ' : new_worker})

def employ_list(request):
    workers = Employee.objects.all()
    return render(request, 'hr/detail.html', {'work' :workers})

def biodata(request, slug):
    bio = Employee.objects.get(slug=slug)
    return render(request, 'hr/biodata.html', {'bio' : bio})

def worker_list(request, section_id):
    employee =  Employee.objects.filter(section_id__id=section_id).order_by('-employee_SN')
    try:
        get_cat_name = Section.objects.get(id=section_id)
    except ObjectDoesNotExist:
        return render(request, 'hr/404.html')
    get_cat_name = Section.objects.get(id=section_id)
    post_cat = Employee.objects.filter(section_id__id=section_id).order_by('-employee_SN')
    context = {'posts': post_cat, 'counts': employee, 'cat': get_cat_name}
    return render(request, 'hr/detail.html', context)