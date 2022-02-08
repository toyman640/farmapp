from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncMonth
from farmrecord.models import *
from django.core.paginator import Paginator


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
    admin_cm = Paginator(cmta, 10)
    page_number = request.GET.get('page')
    acm_page_obj = admin_cm.get_page(page_number)
    nums = "a" * acm_page_obj.paginator.num_pages
    context = {
        'acm_page_obj' : cmta,
        'nums' : nums

    }
    context['acm_page_obj'] = acm_page_obj
    return render(request, 'main/cowmot-a.html', context)

@login_required(login_url='/admin-page/login')
def cow_salea(request):
    csa = CowSale.objects.order_by('-date')
    admin_cs = Paginator(csa, 1)
    page_number = request.GET.get('page')
    acs_page_obj = admin_cs.get_page(page_number)
    nums = "a" * acs_page_obj.paginator.num_pages
    context = {
        'acs_page_obj' : csa,
        'nums' : nums
    }
    context['acs_page_obj'] = acs_page_obj
    return render(request, 'main/cowsale-a.html', context)

@login_required(login_url='/admin-page/login')
def cow_proca(request):
    cpa = CowProcurement.objects.order_by('-date')
    admin_cp = Paginator(cpa, 1)
    page_number = request.GET.get('page')
    acp_page_obj = admin_cp.get_page(page_number)
    nums = "a" * acp_page_obj.paginator.num_pages
    context = {
        'acp_page_obj' : cpa,
        'nums' : nums
    }
    context['acp_page_obj'] = acp_page_obj
    return render(request, 'main/cowproc-a.html', context)

@login_required(login_url='/admin-page/login')
def cow_culla(request):
    cca = CowCulling.objects.order_by('-date')
    paginated_filtercc = Paginator(cca, 1)
    page_number = request.GET.get('page')
    acc_page_obj = paginated_filtercc.get_page(page_number)
    nums = "a" * acc_page_obj.paginator.num_pages
    context = {
        'acc_page_obj' : cca,
        'nums' : nums
    }
    context['acc_page_obj'] = acc_page_obj
    return render(request, 'main/cowcull-a.html', context)

@login_required(login_url='/admin-page/login')
def goat_mota(request):
    gma = GoatMortality.objects.order_by('-date')
    admin_gm = Paginator(gma, 10)
    page_number = request.GET.get('page')
    agm_page_obj = admin_gm.get_page(page_number)
    nums = "a" * agm_page_obj.paginator.num_pages
    context = {
        'agm_page-obj' : gma,
        'nums' : nums
    }
    context['agm_page-obj'] = agm_page_obj
    return render(request, 'main/goatmot-a.html', context)

@login_required(login_url='/admin-page/login')
def goat_salea(request):
    gsa = GoatSale.objects.order_by('-date') 
    admin_gs = Paginator(gsa, 10)
    page_number = request.GET.get('page')
    ags_page_obj = admin_gs.get_page(page_number)
    nums = "a" * ags_page_obj.paginator.num_pages
    context = {
        'ags_page-obj' : gsa,
        'nums' : nums
    }
    context['ags_page-obj'] = ags_page_obj
    return render(request, 'main/goatsale-a.html', context)

@login_required(login_url='/admin-page/login')
def goat_proca(request):
    gpa = GoatProcurement.objects.order_by('-date')
    admin_gp = Paginator(gpa, 10)
    page_number = request.GET.get('page')
    agp_page_obj = admin_gp.get_page(page_number)
    nums = "a" * agp_page_obj.paginator.num_pages
    context = {
        'agp_page-obj' : gpa,
        'nums' : nums
    }
    context['agp_page-obj'] = agp_page_obj
    return render(request, 'main/goatproc-a.html', context)

@login_required(login_url='/admin-page/login')
def goat_culla(request):
    gca = GoatCulling.objects.order_by('-date')
    admin_gc = Paginator(gca, 10)
    page_number = request.GET.get('page')
    agc_page_obj = admin_gc.get_page(page_number)
    nums = "a" * agc_page_obj.paginator.num_pages
    context = {
        'agc_page_obj' : gca,
        'nums' : nums
    }
    context['agc_page_obj'] = agc_page_obj
    return render(request, 'main/goatcull-a.html', context)

@login_required(login_url='/admin-page/login')
def pig_mota(request):
    pma = PigMortality.objects.order_by('-date')
    admin_pm = Paginator(pma, 10)
    page_number = request.GET.get('page')
    apm_page_obj = admin_pm.get_page(page_number)
    nums = "a" * apm_page_obj.paginator.num_pages
    context = {
        'apm_page_obj' : pma,
        'nums' : nums
    }
    context['apm_page_obj'] = apm_page_obj
    return render(request, 'main/pigmot-a.html', context)

@login_required(login_url='/admin-page/login')
def pig_salea(request):
    psa = PigSale.objects.order_by('-date')
    admin_ps = Paginator(psa, 10)
    page_number = request.GET.get('page')
    aps_page_obj = admin_ps.get_page(page_number)
    nums = "a" * aps_page_obj.paginator.num_pages
    context = {
        'aps_page_obj' : psa,
        'nums' : nums
    }
    context['aps_page_obj'] = aps_page_obj
    return render(request, 'main/pigmot-a.html', context)

@login_required(login_url='/admin-page/login')
def pig_proca(request):
    ppa = PigProcurement.objects.order_by('-date')
    admin_pp = Paginator(ppa, 10)
    page_number = request.GET.get('page')
    app_page_obj = admin_pp.get_page(page_number)
    nums = "a" * app_page_obj.paginator.num_pages
    context = {
        'app_page_obj' : ppa,
        'nums' : nums
    }
    context['app_page_obj'] = app_page_obj
    return render(request, 'main/pigproc-a.html', context)

@login_required(login_url='/admin-page/login')
def pig_culla(request):
    pca = PigCulling.objects.order_by('-date')
    admin_pc = Paginator(pca, 10)
    page_number = request.GET.get('page')
    apc_page_obj = admin_pc.get_page(page_number)
    nums = "a" * apc_page_obj.paginator.num_pages
    context = {
        'apc_page_obj' : pca,
        'nums' : nums
    }
    context['apc_page_obj'] = apc_page_obj
    return render(request, 'main/pigcull-a.html', context)

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
    cow_sale = CowSale.objects.all()
    cowsale_total = cow_sale.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('total_price'))
    context = {
        'motcc' : chart_countc,
        'popc' : popad,
        'bullc' : bullM_count,
        'cowc' : cowM_count,
        'calfc' : calf_count,
        'bullcull' : bullC_count,
        'cowcull' : cowC_count,
        'cowsale' : cowsale_total
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
    goat_sale = GoatSale.objects.all()
    goat_total = goat_sale.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('total_price'))
    context = {
        'motcg' : chart_countg,
        'popg' : popadg,
        'buckc' : buckM_count,
        'doec' : doeM_count,
        'kidc' : kid_count,
        'buckcull' : buckC_count,
        'doecull' : doeC_count,
        'goatsale' : goat_total
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
    pig_sale = PigSale.objects.all()
    pig_total = pig_sale.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('total_price'))
    context = {
        'motcp' : chart_countp,
        'popp' : popadp,
        'boarc' : boarM_count,
        'sowc' : sowM_count,
        'piggletc' : pigglet_count,
        'boarcull' : boarC_count,
        'sowcull' : sowC_count,
        'pigsale' : pig_total
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
    sheep_sale = SheepSale.objects.all()
    sheep_total = sheep_sale.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('total_price'))
    context = {
        'motcs' : chart_counts,
        'pops' : popads,
        'ramc' : ramM_count,
        'ewec' : eweM_count,
        'lambc' : lamb_count,
        'ramcull' : ramC_count,
        'ewecull' : eweC_count,
        'sheepsale' : sheep_total
    }
    return render(request, 'main/sheep-allad.html', context)