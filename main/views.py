from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from farmrecord.models import *

# Create your views here.

@login_required(login_url='/admin-page/login')
def dashboard(request):
    return render(request, 'main/index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('main:dashboard')
            else:
                return redirect('farmrecord:index')
        else:
            messages.info(request, 'Username OR Password is incorrect')
           
    return render(request, 'main/login.html')

@login_required(login_url='/admin-page/login')
def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='/admin-page/login')
def latest_page(request):
    cowmot = CowMortality.objects.order_by('-date')[:1]
    goatmot = GoatMortality.objects.order_by('-date')[:1]
    sheepmot= SheepMortality.objects.order_by('-date')[:1]
    pigmot = PigMortality.objects.order_by('-date')[:1]
    cowsale = CowSale.objects.order_by('-date')[:1]
    goatsale = GoatSale.objects.order_by('-date')[:1]
    pigsale = PigSale.objects.order_by('-date')[:1]
    sheepsale = SheepSale.objects.order_by('-date')[:1]
    cowproc = CowProcurement.objects.order_by('-date')[:1]
    goatproc = GoatProcurement.objects.order_by('-date')[:1]
    sheepproc = SheepProcurement.objects.order_by('-date')[:1]
    pigproc = PigProcurement.objects.order_by('-date')[:1]
    cowcull = CowCulling.objects.order_by('-date')[:1]
    pigcull = PigCulling.objects.order_by('-date')[:1]
    goatcull = GoatCulling.objects.order_by('-date')[:1]
    sheepcull = SheepCulling.objects.order_by('-date')[:1]
    context = {
        'cml' : cowmot,
        'gml' : goatmot,
        'pml' : pigmot,
        'sml' : sheepmot,
        'csl' : cowsale,
        'psl' : pigsale,
        'gsl' : goatsale,
        'ssl' : sheepsale,
        'spl' : sheepproc,
        'cpl' : cowproc,
        'gpl' : goatproc,
        'ppl' : pigproc,
        'ccl' : cowcull,
        'gcl' : goatcull,
        'pcl' : pigcull,
        'scl' : sheepcull

    }

    return render (request, 'main/latest-rep-animal.html', context)

@login_required(login_url='/admin-page/login')
def cow_mota(request):
    cmta = CowMortality.objects.order_by('-date')
    return render(request, 'main/cowmot-a.html', {'cmta' : cmta})

@login_required(login_url='/admin-page/login')
def cow_salea(request):
    csa = CowSale.objects.order_by('-date')
    return render(request, 'main/cowsale-a.html', {'csa': csa})

@login_required(login_url='/admin-page/login')
def cow_proca(request):
    cpa = CowProcurement.objects.order_by('-date')
    return render(request, 'main/cowproc-a.html', {'cpa' : cpa})

@login_required(login_url='/admin-page/login')
def cow_culla(request):
    cca = CowCulling.objects.order_by('-date')
    return render(request, 'cowcull-a.html', {'cca': cca})

@login_required(login_url='/admin-page/login')
def goat_mota(request):
    pass

@login_required(login_url='/admin-page/login')
def goat_salea(request):
    pass

@login_required(login_url='/admin-page/login')
def goat_proca(request):
    pass

@login_required(login_url='/admin-page/login')
def goat_culla(request):
    pass

@login_required(login_url='/admin-page/login')
def pig_mota(request):
    pass

@login_required(login_url='/admin-page/login')
def pig_salea(request):
    pass

@login_required(login_url='/admin-page/login')
def pig_proca(request):
    pass

@login_required(login_url='/admin-page/login')
def pig_culla(request):
    pass

@login_required(login_url='/admin-page/login')
def sheep_mota(request):
    pass

@login_required(login_url='/admin-page/login')
def sheep_salea(request):
    pass

@login_required(login_url='/admin-page/login')
def sheep_proca(request):
    pass

@login_required(login_url='/admin-page/login')
def sheep_culla(request):
    pass