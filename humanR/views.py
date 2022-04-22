from tkinter import E
from turtle import title
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from farmrecord.models import Section
from humanR.models import *
from farmrecord.forms import EmployeeFilter, WorkerForm
from django.contrib import messages
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='/admin-page/login')
def index(request):
    worker = Employee.objects.all().count()
    section = FarmSection.objects.all().annotate(sec_count=Count('employee'))
    check_worker = EmployeeFilter()
    return render(request, 'hr/index.html', {'section': section, 'worker' : worker, 'check' : check_worker})

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


def worker_check(request):
    qs = Employee.objects.all()
    if request.method == 'GET':
        search_form = EmployeeFilter(request.GET)
        if search_form.is_valid():
            surname = search_form.cleaned_data.get('employee_SN')
            name = search_form.cleaned_data.get('employee_FN')
            section = search_form.cleaned_data.get('section_id')
            title = search_form.cleaned_data.get('title_id')

            if surname != '' and surname is not None:
                qs = qs.filter(employee_SN__icontains=surname)
            if name != '' and name is not None:
                qs = qs.filter(employee_FN__icontains=name)
            
            if section != '' and section is not None:
                qs = qs.filter(section_id__section_name__contains=section)
            
            if title != '' and title is not None:
                qs = qs.filter(title_id__title_name__contains=title)
            return render(request, 'hr/search-page.html', {'result': qs})
        else:
            return render(request, 'hr/search-page.html')


def calculator(request):
    res = 0
    if request.method == "POST":
        num1 = request.POST.get('days')
        num2 = request.POST.get('salary')
        num3 = request.POST.get('tax')

        if num1.isdigit() and num2.isdigit() and num3.isdigit():
            a = int(num1)
            b = int(num2)
            c = int(num3)

            first = b / 30
            
            second = int(first) * a
            
            res = int(second) - c

        
    
    

        if request.headers.get('Hx-Request') == 'true':
            return HttpResponse(str(res))

    else:
        res = "Only digits are allowed"

    
    return render(request, 'hr/calculator.html')