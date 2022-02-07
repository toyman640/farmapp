from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncMonth
from farmrecord.models import *
import math
from django.db.models import ExpressionWrapper

# Create your views here.

@login_required(login_url='/admin-page/login')
def dashboard(request):
    cowpop = CowCensusPop.objects.order_by('-date')
    pigpop = PigCensusPop.objects.order_by('-date')
    sheeppop = SheepCensusPop.objects.order_by('-date')
    goatpop = GoatCensusPop.objects.order_by('-date')
    context ={
        'ctotal' : cowpop,
        'ptotal' : pigpop,
        'stotal' : sheeppop,
        'gtotal' : goatpop
    }
    return render(request, 'main/index.html', context)

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
    return render(request, 'main/cowmot-a.html', {'my_cmta' : cmta})

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
    return render(request, 'main/cowcull-a.html', {'cca': cca})

@login_required(login_url='/admin-page/login')
def goat_mota(request):
    gma = GoatMortality.objects.order_by('-date')
    return render(request, 'main/goatmot-a.html', {'gma' : gma})

@login_required(login_url='/admin-page/login')
def goat_salea(request):
    gsa = GoatSale.objects.order_by('-date') 
    return render(request, 'main/goatsale-a.html', {'gsa' : gsa})

@login_required(login_url='/admin-page/login')
def goat_proca(request):
    gpa = GoatProcurement.objects.order_by('-date')
    return render(request, 'main/goatproc-a.html', {'gpa' : gpa})

@login_required(login_url='/admin-page/login')
def goat_culla(request):
    gca = GoatCulling.objects.order_by('-date')
    return render(request, 'main/goatcull-a.html', {'gca' : gca})

@login_required(login_url='/admin-page/login')
def pig_mota(request):
    pma = PigMortality.objects.order_by('-date')
    return render(request, 'main/pigmot-a.html', {'pma' : pma})

@login_required(login_url='/admin-page/login')
def pig_salea(request):
    psa = PigSale.objects.order_by('-date')
    return render(request, 'main/pigmot-a.html', {'psa' : psa})

@login_required(login_url='/admin-page/login')
def pig_proca(request):
    ppa = PigProcurement.objects.order_by('-date')
    return render(request, 'main/pigproc-a.html', {'ppa' : ppa})

@login_required(login_url='/admin-page/login')
def pig_culla(request):
    pca = PigCulling.objects.order_by('-date')
    return render(request, 'main/pigcull-a.html', {'pca' : pca})

@login_required(login_url='/admin-page/login')
def sheep_mota(request):
    sma = SheepMortality.objects.order_by('-date')
    return render(request, 'main/sheepmot-a.html', {'sma' : sma})

@login_required(login_url='/admin-page/login')
def sheep_salea(request):
    ssa = SheepSale.objects.order_by('-date')
    return render(request, 'main/sheepsale-a.html', {'ssa' : ssa})

@login_required(login_url='/admin-page/login')
def sheep_proca(request):
    spa = SheepProcurement.objects.order_by('-date')
    return render(request, 'main/sheepproc-a.html', {'spa' : spa})

@login_required(login_url='/admin-page/login')
def sheep_culla(request):
    sca = SheepCulling.objects.order_by('-date')
    return render(request, 'main/sheepcull-a.html', {'sca' : sca})

@login_required(login_url='/admin-page/login')
def cow_all(request):
    c_chart = CowMortality.objects.all()
    chart_countc = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    bullM_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('bull_num'))
    cowM_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('cow_num'))
    calf_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('calves'))
    popad = CowCensusPop.objects.order_by('-date')[:12]
    cullcow = CowCulling.objects.all()
    bullC_count = cullcow.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('bull_num'))
    cowC_count = cullcow.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('cow_num'))
    context = {
        'motcc' : chart_countc,
        'popc' : popad,
        'bullc' : bullM_count,
        'cowc' : cowM_count,
        'calfc' : calf_count,
        'bullcull' : bullC_count,
        'cowcull' : cowC_count
    }
    return render(request, 'main/cow-allad.html', context)

@login_required(login_url='/admin-page/login')
def goat_all(request):
    g_chart = GoatMortality.objects.all()
    chart_countg = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    buckM_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('buck_num'))
    doeM_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('doe_num'))
    kid_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('kid'))
    popadg = GoatCensusPop.objects.order_by('-date')[:12]
    cullgoat = GoatCulling.objects.all()
    buckC_count = cullgoat.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('buck_num'))
    doeC_count = cullgoat.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('doe_num'))
    context = {
        'motcg' : chart_countg,
        'popg' : popadg,
        'buckc' : buckM_count,
        'doec' : doeM_count,
        'kidc' : kid_count,
        'buckcull' : buckC_count,
        'doecull' : doeC_count
    }
    return render(request, 'main/goat-allad.html', context)

@login_required(login_url='/admin-page/login')
def pig_all(request):
    p_chart = PigMortality.objects.all()
    chart_countp = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    boarM_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('boar_num'))
    sowM_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('sow_num'))
    pigglet_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('pigglet'))
    popadp = PigCensusPop.objects.order_by('-date')[:12]
    cullpig = PigCulling.objects.all()
    boarC_count = cullpig.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('boar_num'))
    sowC_count = cullpig.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('sow_num'))
    context = {
        'motcp' : chart_countp,
        'popp' : popadp,
        'boarc' : boarM_count,
        'sowc' : sowM_count,
        'piggletc' : pigglet_count,
        'boarcull' : boarC_count,
        'sowcull' : sowC_count
    }
    return render(request, 'main/pig-allad.html', context)

@login_required(login_url='/admin-page/login')
def sheep_all(request):
    s_chart = SheepMortality.objects.all()
    chart_counts = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    ramM_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ram_num'))
    eweM_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ewe_num'))
    lamb_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('lamb'))
    popads = SheepCensusPop.objects.order_by('-date')[:12]
    cullsheep = SheepCulling.objects.all()
    ramC_count = cullsheep.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ram_num'))
    eweC_count = cullsheep.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ewe_num'))
    context = {
        'motcs' : chart_counts,
        'pops' : popads,
        'ramc' : ramM_count,
        'ewec' : eweM_count,
        'lambc' : lamb_count,
        'ramcull' : ramC_count,
        'ewecull' : eweC_count
    }
    return render(request, 'main/sheep-allad.html', context)