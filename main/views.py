from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncMonth
from farmrecord.models import *
from django.core.paginator import Paginator
from farmrecord.forms import *
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


@staff_required(login_url="/admin-page/login")
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

# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 return redirect('main:dashboard')
#             else:
#                 return redirect('farmrecord:index')
#         else:
#             messages.info(request, 'Username OR Password is incorrect')
           
#     return render(request, 'main/login.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.profile.is_boss:
            login(request, user)
            return redirect('main:dashboard')
        elif user is not None and user.profile.is_supervisor:
            login(request, user)
            return redirect('farmrecord:index')
            
        else:
            messages.info(request, 'Username OR Password is incorrect')
           
    return render(request, 'main/login.html')

@staff_required(login_url="/admin-page/login")
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login_page')


@staff_required(login_url="/admin-page/login")
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

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_mota(request):
    cmta = CowMortality.objects.order_by('-date')
    query_form = CowmotFilter()
    admin_cm = Paginator(cmta, 1)
    page_number = request.GET.get('page')
    acm_page_obj = admin_cm.get_page(page_number)
    nums = "a" * acm_page_obj.paginator.num_pages
    context = {
        'acm_page_obj' : cmta,
        'nums' : nums,
        'cma' : query_form,
        'active' : page_number

    }
    context['acm_page_obj'] = acm_page_obj
    return render(request, 'main/cowmot-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_image_view(request, slug):
    aview = CowMortality.objects.get(slug=slug)
    return render(request, 'main/cowmot-aview.html', {'cmview':aview})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goat_image_view(request, slug):
    aview = GoatMortality.objects.get(slug=slug)
    return render(request, 'main/goatmot-aview.html', {'gmview':aview})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheep_image_view(request, slug):
    aview = SheepMortality.objects.get(slug=slug)
    return render(request, 'main/sheepmot-aview.html', {'smview':aview})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pig_image_view(request, slug):
    aview = PigMortality.objects.get(slug=slug)
    return render(request, 'main/pigmot-aview.html', {'pmview':aview})


@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_salea(request):
    csa = CowSale.objects.order_by('-date')
    query_form = CowsaleFilter()
    admin_cs = Paginator(csa, 1)
    page_number = request.GET.get('page')
    acs_page_obj = admin_cs.get_page(page_number)
    nums = "a" * acs_page_obj.paginator.num_pages
    context = {
        'acs_page_obj' : csa,
        'nums' : nums,
        'csa' : query_form
    }
    context['acs_page_obj'] = acs_page_obj
    return render(request, 'main/cowsale-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_proca(request):
    cpa = CowProcurement.objects.order_by('-date')
    query_form = CowprocFilter()
    admin_cp = Paginator(cpa, 1)
    page_number = request.GET.get('page')
    acp_page_obj = admin_cp.get_page(page_number)
    nums = "a" * acp_page_obj.paginator.num_pages
    context = {
        'acp_page_obj' : cpa,
        'nums' : nums,
        'cpa' : query_form
    }
    context['acp_page_obj'] = acp_page_obj
    return render(request, 'main/cowproc-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_culla(request):
    cca = CowCulling.objects.order_by('-date')
    query_form = CowcullFilter()
    paginated_filtercc = Paginator(cca, 1)
    page_number = request.GET.get('page')
    acc_page_obj = paginated_filtercc.get_page(page_number)
    nums = "a" * acc_page_obj.paginator.num_pages
    context = {
        'acc_page_obj' : cca,
        'nums' : nums,
        'cca' : query_form
    }
    context['acc_page_obj'] = acc_page_obj
    return render(request, 'main/cowcull-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goat_mota(request):
    gma = GoatMortality.objects.order_by('-date')
    query_form = GoatmotFilter()
    admin_gm = Paginator(gma, 1)
    page_number = request.GET.get('page', 1)
    agm_page_obj = admin_gm.get_page(page_number)
    nums = "a" * agm_page_obj.paginator.num_pages
    context = {
        'agm_page_obj' : gma,
        'nums' : nums,
        'page_number' : int(page_number),
        'gma' : query_form
    } 
    context['agm_page_obj'] = agm_page_obj
    return render(request, 'main/goatmot-a.html', context) 

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goat_salea(request):
    gsa = GoatSale.objects.order_by('-date')
    query_form = GoatsaleFilter()
    admin_gs = Paginator(gsa, 10)
    page_number = request.GET.get('page')
    ags_page_obj = admin_gs.get_page(page_number)
    nums = "a" * ags_page_obj.paginator.num_pages
    context = {
        'ags_page-obj' : gsa,
        'nums' : nums,
        'gsa' : query_form
    }
    context['ags_page_obj'] = ags_page_obj
    return render(request, 'main/goatsale-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goat_proca(request):
    gpa = GoatProcurement.objects.order_by('-date')
    query_form = GoatprocFilter()
    admin_gp = Paginator(gpa, 10)
    page_number = request.GET.get('page', 1)
    agp_page_obj = admin_gp.get_page(page_number)
    nums = "a" * agp_page_obj.paginator.num_pages
    context = {
        'agp_page-obj' : gpa,
        'nums' : nums,
        'page_number' : int(page_number),
        'gpa' : query_form
    }
    context['agp_page_obj'] = agp_page_obj
    return render(request, 'main/goatproc-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goat_culla(request):
    gca = GoatCulling.objects.order_by('-date')
    query_form = GoatcullFilter()
    admin_gc = Paginator(gca, 10)
    page_number = request.GET.get('page')
    agc_page_obj = admin_gc.get_page(page_number)
    nums = "a" * agc_page_obj.paginator.num_pages
    context = {
        'agc_page_obj' : gca,
        'nums' : nums,
        'gca' : query_form
    }
    context['agc_page_obj'] = agc_page_obj
    return render(request, 'main/goatcull-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pig_mota(request):
    pma = PigMortality.objects.order_by('-date')
    query_form = PigmotFilter()
    admin_pm = Paginator(pma, 10)
    page_number = request.GET.get('page')
    apm_page_obj = admin_pm.get_page(page_number)
    nums = "a" * apm_page_obj.paginator.num_pages
    context = {
        'apm_page_obj' : pma,
        'nums' : nums,
        'pma' : query_form
    }
    context['apm_page_obj'] = apm_page_obj
    return render(request, 'main/pigmot-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pig_salea(request):
    psa = PigSale.objects.order_by('-date')
    query_form = PigsaleFilter()
    admin_ps = Paginator(psa, 10)
    page_number = request.GET.get('page')
    aps_page_obj = admin_ps.get_page(page_number)
    nums = "a" * aps_page_obj.paginator.num_pages
    context = {
        'aps_page_obj' : psa,
        'nums' : nums,
        'psa' : query_form
    }
    context['aps_page_obj'] = aps_page_obj
    return render(request, 'main/pigmot-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pig_proca(request):
    ppa = PigProcurement.objects.order_by('-date')
    query_form = PigprocFilter()
    admin_pp = Paginator(ppa, 10)
    page_number = request.GET.get('page')
    app_page_obj = admin_pp.get_page(page_number)
    nums = "a" * app_page_obj.paginator.num_pages
    context = {
        'app_page_obj' : ppa,
        'nums' : nums,
        'ppa' : query_form
    }
    context['app_page_obj'] = app_page_obj
    return render(request, 'main/pigproc-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pig_culla(request):
    pca = PigCulling.objects.order_by('-date')
    query_form = PigcullFilter() 
    admin_pc = Paginator(pca, 10)
    page_number = request.GET.get('page')
    apc_page_obj = admin_pc.get_page(page_number)
    nums = "a" * apc_page_obj.paginator.num_pages
    context = {
        'apc_page_obj' : pca,
        'nums' : nums,
        'pca' : query_form
    }
    context['apc_page_obj'] = apc_page_obj
    return render(request, 'main/pigcull-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheep_mota(request):
    sma = SheepMortality.objects.order_by('-date')
    query_form = SheepmotFilter()
    admin_sm = Paginator(sma, 10)
    page_number = request.GET.get('page')
    asm_page_obj = admin_sm.get_page(page_number)
    nums = "a" * asm_page_obj.paginator.num_pages
    context = {
        'asm_page_obj' : sma,
        'nums' : nums,
        'sma' : query_form
    }
    context['asm_page_obj'] = asm_page_obj
    return render(request, 'main/sheepmot-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheep_salea(request):
    ssa = SheepSale.objects.order_by('-date')
    query_form = SheepsaleFilter()
    admin_ss = Paginator(ssa, 10)
    page_number = request.GET.get('page')
    ass_page_obj = admin_ss.get_page(page_number)
    nums = "a" * ass_page_obj.paginator.num_pages
    context = {
        'ass_page_obj' : ssa,
        'nums' : nums,
        'ssa' : query_form
    }
    context['ass_page_obj'] = ass_page_obj
    return render(request, 'main/sheepsale-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheep_proca(request):
    spa = SheepProcurement.objects.order_by('-date')
    query_form = SheepprocFilter()
    admin_sp = Paginator(spa, 10)
    page_number = request.GET.get('page')
    asp_page_obj = admin_sp.get_page(page_number)
    nums = "a" * asp_page_obj.paginator.num_pages
    context = {
        'asp_page_obj' : spa,
        'nums' : nums,
        'spa' : query_form
    }
    context['asp_page_obj'] = asp_page_obj
    return render(request, 'main/sheepproc-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheep_culla(request):
    sca = SheepCulling.objects.order_by('-date')
    query_form = SheepcullFilter()
    admin_sc = Paginator(sca, 10)
    page_number = request.GET.get('page')
    asc_page_obj = admin_sc.get_page(page_number)
    nums = "a" * asc_page_obj.paginator.num_pages
    context = {
        'asc_page_obj' : sca,
        'nums' : nums,
        'sca' : query_form
    }
    context['asc_page_obj'] = asc_page_obj
    return render(request, 'main/sheepcull-a.html', context)

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cow_all(request):
    c_chart = CowMortality.objects.all()
    chart_countc = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    bullM_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('bull_num'))
    cowM_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('cow_num'))
    calf_count = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('calves'))
    popad = CowCensusPop.objects.order_by('-date').reverse()[:5]
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

@staff_required(login_url="/admin-page/login")
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

@staff_required(login_url="/admin-page/login")
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

@staff_required(login_url="/admin-page/login")
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

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cowmota_filter(request):
    if request.method == 'GET':
        cowmot_querya = CowmotFilter(request.GET)
        if cowmot_querya.is_valid():
            start_date = cowmot_querya.cleaned_data.get('start_date')
            end_date = cowmot_querya.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowMortality.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-cowmot.html', {'queryseta': result, 'cma': cowmot_querya, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        cowmot_querya = CowmotFilter()
    return render(request, 'main/afilter-cowmot.html', {'cma': cowmot_querya})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goatmota_filter(request):
    if request.method == 'GET':
        goatmot_query = GoatmotFilter(request.GET)
        if goatmot_query.is_valid():
            start_date = goatmot_query.cleaned_data.get('start_date')
            end_date = goatmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatMortality.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-goatmot.html', {'queryseta': result, 'gma': goatmot_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        goatmot_query = GoatmotFilter()
    return render(request, 'main/afilter-goatmot.html', {'gma': goatmot_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pigmota_filter(request):
    if request.method == 'GET':
        pigmot_query = PigmotFilter(request.GET)
        if pigmot_query.is_valid():
            start_date = pigmot_query.cleaned_data.get('start_date')
            end_date = pigmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigMortality.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-pigmot.html', {'queryseta': result, 'pma': pigmot_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        pigmot_query = PigmotFilter()
    return render(request, 'main/afilter-pigmot.html', {'pma': pigmot_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheepmota_filter(request):
    if request.method == 'GET':
        sheepmot_query = SheepmotFilter(request.GET)
        if sheepmot_query.is_valid():
            start_date = sheepmot_query.cleaned_data.get('start_date')
            end_date = sheepmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepMortality.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-sheepmot.html', {'queryseta': result, 'sma': sheepmot_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepmot_query = SheepmotFilter()
    return render(request, 'main/afilter-sheepmot.html', {'q': sheepmot_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheepsalea_filter(request):
    if request.method == 'GET':
        sheepsale_query = SheepsaleFilter(request.GET)
        if sheepsale_query.is_valid():
            start_date = sheepsale_query.cleaned_data.get('start_date')
            end_date = sheepsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepSale.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-sheepsale.html', {'queryseta': result, 'ssa': sheepsale_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepsale_query = SheepsaleFilter()
    return render(request, 'main/afilter-sheepsale.html', {'ssa': sheepsale_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pigsalea_filter(request):
    if request.method == 'GET':
        pigsale_query = PigsaleFilter(request.GET)
        if pigsale_query.is_valid():
            start_date = pigsale_query.cleaned_data.get('start_date')
            end_date = pigsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigSale.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-pigsale.html', {'queryseta': result, 'psa': pigsale_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        pigsale_query = PigsaleFilter()
    return render(request, 'main/afilter-pigsale.html', {'psa': pigsale_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cowsalea_filter(request):
    if request.method == 'GET':
        cowsale_query = CowsaleFilter(request.GET)
        if cowsale_query.is_valid():
            start_date = cowsale_query.cleaned_data.get('start_date')
            end_date = cowsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowSale.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-cowsale.html', {'queryseta': result, 'csa': cowsale_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        cowsale_query = CowsaleFilter()
    return render(request, 'main/afilter-cowsale.html', {'csa': cowsale_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goatsalea_filter(request):
    if request.method == 'GET':
        goatsale_query = GoatsaleFilter(request.GET)
        if goatsale_query.is_valid():
            start_date = goatsale_query.cleaned_data.get('start_date')
            end_date = goatsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatSale.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-sheepsale.html', {'queryseta': result, 'gsa': goatsale_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        goatsale_query = GoatsaleFilter()
    return render(request, 'main/afilter-sheepsale.html', {'gsa': goatsale_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheepproca_filter(request):
    if request.method == 'GET':
        sheepproc_query = SheepprocFilter(request.GET)
        if sheepproc_query.is_valid():
            start_date = sheepproc_query.cleaned_data.get('start_date')
            end_date = sheepproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepProcurement.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-sheepproc.html', {'queryseta': result, 'spa': sheepproc_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepproc_query = SheepprocFilter()
    return render(request, 'main/afilter-sheepproc.html', {'spa': sheepproc_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pigproca_filter(request):
    if request.method == 'GET':
        pigproc_query = PigprocFilter(request.GET)
        if pigproc_query.is_valid():
            start_date = pigproc_query.cleaned_data.get('start_date')
            end_date = pigproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigProcurement.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-pigproc.html', {'queryseta': result, 'ppa': pigproc_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        pigproc_query = PigprocFilter()
    return render(request, 'main/filter-pigproc.html', {'ppa': pigproc_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cowproca_filter(request):
    if request.method == 'GET':
        cowproc_query = CowprocFilter(request.GET)
        if cowproc_query.is_valid():
            start_date = cowproc_query.cleaned_data.get('start_date')
            end_date = cowproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowProcurement.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-cowproc.html', {'queryseta': result, 'cpa': cowproc_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        cowproc_query = CowprocFilter()
    return render(request, 'main/afilter-sheepproc.html', {'cpa': cowproc_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goatproca_filter(request):
    if request.method == 'GET':
        goatproc_query = GoatprocFilter(request.GET)
        if goatproc_query.is_valid():
            start_date = goatproc_query.cleaned_data.get('start_date')
            end_date = goatproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatProcurement.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-goatproc.html', {'queryseta': result, 'gpa': goatproc_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        goatproc_query = GoatprocFilter()
    return render(request, 'main/afilter-goatproc.html', {'gpa': goatproc_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def cowculla_filter(request):
    if request.method == 'GET':
        cowcull_query = CowcullFilter(request.GET)
        if cowcull_query.is_valid():
            start_date = cowcull_query.cleaned_data.get('start_date')
            end_date = cowcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowCulling.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-cowcull.html', {'queryseta': result, 'cca': cowcull_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        cowcull_query = CowcullFilter()
    return render(request, 'main/afilter-cowcull.html', {'cca': cowcull_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def goatculla_filter(request):
    if request.method == 'GET':
        goatcull_query = GoatcullFilter(request.GET)
        if goatcull_query.is_valid():
            start_date = goatcull_query.cleaned_data.get('start_date')
            end_date = goatcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatCulling.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-goatcull.html', {'queryseta': result, 'gca': goatcull_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        goatcull_query = GoatcullFilter()
    return render(request, 'main/afilter-goatcull.html', {'gca': goatcull_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def sheepculla_filter(request):
    if request.method == 'GET':
        sheepcull_query = SheepcullFilter(request.GET)
        if sheepcull_query.is_valid():
            start_date = sheepcull_query.cleaned_data.get('start_date')
            end_date = sheepcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepCulling.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-sheepcull.html', {'queryseta': result, 'sca': sheepcull_query, 'count' : count})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepcull_query = SheepcullFilter()
    return render(request, 'main/afilter-sheepcull.html', {'sca': sheepcull_query})

@staff_required(login_url="/admin-page/login")
@login_required(login_url='/admin-page/login')
def pigculla_filter(request):
    if request.method == 'GET':
        pigcull_query = PigcullFilter(request.GET)
        if pigcull_query.is_valid():
            start_date = pigcull_query.cleaned_data.get('start_date')
            end_date = pigcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigCulling.objects.filter(date__range=[start_date, new_end])
            count = result.count()
            return render(request, 'main/afilter-pigcull.html', {'queryseta': result, 'pca': pigcull_query, 'count' : count })
        else:
            messages.error(request, 'Out of range')
    else:
        pigcull_query = PigcullFilter()
    return render(request, 'main/afilter-pigcull.html', {'pca': pigcull_query})