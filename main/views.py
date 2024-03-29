from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncMonth, TruncDay
from farmrecord.models import *
from django.core.paginator import Paginator
from farmrecord.forms import *
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from humanR.models import FarmSection, Employee
from datetime import datetime

today = datetime.today()

year = today.year
month = today.month
day = today.day


# Create your views here.

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


@staff_required(login_url="/")
@login_required(login_url='/')
def dashboard(request):
    current_datetime = datetime.now()
    current_month = datetime.now().month
    cowpop = CowCensusPop.objects.order_by('-date')
    pigpop = PigCensusPop.objects.order_by('-date')
    sheeppop = SheepCensusPop.objects.order_by('-date')
    goatpop = GoatCensusPop.objects.order_by('-date')
    worker = Employee.objects.all().count()
    section = FarmSection.objects.all().annotate(sec_count=Count('employee'))
    # cattle mortality daily
    today_cow_mortality = CowMortality.objects.filter(date__date=timezone.now().date())
    total_cow = today_cow_mortality.aggregate(Sum('cow_num'))['cow_num__sum'] or 0
    total_bull = today_cow_mortality.aggregate(Sum('bull_num'))['bull_num__sum'] or 0
    total_calves = today_cow_mortality.aggregate(Sum('calves'))['calves__sum'] or 0
    total_cattle_mortality = total_cow + total_bull + total_calves
    # calttle birth daily
    today_cow_birth = CowBirth.objects.filter(date__date=timezone.now().date())
    total_clavings = today_cow_birth.aggregate(Sum('clavings_num'))['clavings_num__sum'] or 0
    # cattle cull daily
    today_cow_cull = CowCulling.objects.filter(date__date=timezone.now().date())
    total_cow_cullings = today_cow_cull.aggregate(Sum('cow_num'))['cow_num__sum'] or 0
    total_bull_cullings = today_cow_cull.aggregate(Sum('bull_num'))['bull_num__sum'] or 0
    total_cow_cull = total_cow_cullings + total_bull_cullings
    # cattle procurement daily
    today_cow_proc = CowProcurement.objects.filter(date__date=timezone.now().date())
    total_cow_procurements = today_cow_proc.aggregate(Sum('cow_num'))['cow_num__sum'] or 0
    total_bull_procurements = today_cow_proc.aggregate(Sum('bull_num'))['bull_num__sum'] or 0
    total_cattle_procurements = total_bull_procurements + total_cow_procurements
    # pig mortality daily
    today_pig_mortalities = PigMortality.objects.filter(date__date=timezone.now().date())
    total_sow_mot = today_pig_mortalities.aggregate(Sum('sow_num'))['sow_num__sum'] or 0
    total_boar_mot = today_pig_mortalities.aggregate(Sum('boar_num'))['boar_num__sum'] or 0
    total_nursing_mot = today_pig_mortalities.aggregate(Sum('nursing_num'))['nursing_num__sum'] or 0
    total_hogs_mot = today_pig_mortalities.aggregate(Sum('hogs_num'))['hogs_num__sum'] or 0
    total_growers_mot = today_pig_mortalities.aggregate(Sum('growers_num'))['growers_num__sum'] or 0
    total_weaners_mot = today_pig_mortalities.aggregate(Sum('weaners_num'))['weaners_num__sum'] or 0
    total_drysows_mot = today_pig_mortalities.aggregate(Sum('drysows_num'))['drysows_num__sum'] or 0
    total_pigglet_mot = today_pig_mortalities.aggregate(Sum('pigglet'))['pigglet__sum'] or 0
    total_pig_mortality = total_sow_mot + total_boar_mot + total_nursing_mot + total_hogs_mot + total_growers_mot + total_weaners_mot + total_drysows_mot + total_pigglet_mot
    # pig culling daily
    today_pig_cullings = PigCulling.objects.filter(date__date=timezone.now().date())
    total_sow_cull = today_pig_cullings.aggregate(Sum('sow_num'))['sow_num__sum'] or 0
    total_boar_cull = today_pig_cullings.aggregate(Sum('boar_num'))['boar_num__sum'] or 0
    total_pig_cull = total_sow_cull + total_boar_cull
    # pig procurement daily
    today_pig_procurements = PigProcurement.objects.filter(date__date=timezone.now().date())
    total_sow_proc = today_pig_procurements.aggregate(Sum('sow_num'))['sow_num__sum'] or 0
    total_boar_proc = today_pig_procurements.aggregate(Sum('boar_num'))['boar_num__sum'] or 0
    total_pig_proc = total_sow_proc + total_boar_proc
    # pig birth daily
    today_pig_births = PigBirth.objects.filter(date__date=timezone.now().date())
    total_farrowing = today_pig_births.aggregate(Sum('farrowing_num'))['farrowing_num__sum'] or 0
    # sheep mortality daily
    today_sheep_mortalities = SheepMortality.objects.filter(date__date=timezone.now().date())
    total_ewe_mot = today_sheep_mortalities.aggregate(Sum('ewe_num'))['ewe_num__sum'] or 0
    total_ram_mot = today_sheep_mortalities.aggregate(Sum('ram_num'))['ram_num__sum'] or 0
    total_lamb_mot = today_sheep_mortalities.aggregate(Sum('lamb'))['lamb__sum'] or 0
    total_sheep_mot = total_ewe_mot + total_ram_mot + total_lamb_mot
    # sheep cull daily
    today_sheep_cullings = SheepCulling.objects.filter(date__date=timezone.now().date())
    total_ewe_cull = today_sheep_cullings.aggregate(Sum('ewe_num'))['ewe_num__sum'] or 0
    total_ram_cull = today_sheep_cullings.aggregate(Sum('ram_num'))['ram_num__sum'] or 0
    total_sheep_cull = total_ewe_cull + total_ram_cull
    # sheep procurement daily
    today_sheep_procurements = SheepProcurement.objects.filter(date__date=timezone.now().date())
    total_ewe_proc = today_sheep_procurements.aggregate(Sum('ewe_num'))['ewe_num__sum'] or 0
    total_ram_proc = today_sheep_procurements.aggregate(Sum('ram_num'))['ram_num__sum'] or 0
    total_sheep_proc = total_ewe_proc + total_ram_proc
    # sheep birth daily
    today_sheep_births = SheepBirth.objects.filter(date__date=timezone.now().date())
    total_lambing = today_sheep_births.aggregate(Sum('lambings_num'))['lambings_num__sum'] or 0
    # goat mortality daily
    today_goat_mortalities = GoatMortality.objects.filter(date__date=timezone.now().date())
    total_doe_mot = today_goat_mortalities.aggregate(Sum('doe_num'))['doe_num__sum'] or 0
    total_buck_mot = today_goat_mortalities.aggregate(Sum('buck_num'))['buck_num__sum'] or 0
    total_kid_mot = today_goat_mortalities.aggregate(Sum('kid'))['kid__sum'] or 0
    total_goat_mot = total_doe_mot + total_buck_mot + total_kid_mot
    # goat culling daily
    today_goat_cullings = GoatCulling.objects.filter(date__date=timezone.now().date())
    total_doe_cull = today_goat_cullings.aggregate(Sum('doe_num'))['doe_num__sum'] or 0
    total_buck_cull = today_goat_cullings.aggregate(Sum('buck_num'))['buck_num__sum'] or 0
    total_goat_cull = total_doe_cull + total_buck_cull
    # goat procurement daily
    today_goat_procurements = GoatProcurement.objects.filter(date__date=timezone.now().date())
    total_doe_proc = today_goat_procurements.aggregate(Sum('doe_num'))['doe_num__sum'] or 0
    total_buck_proc = today_goat_procurements.aggregate(Sum('buck_num'))['buck_num__sum'] or 0
    total_goat_proc = total_doe_proc + total_buck_proc
    # goat birth daily
    today_goat_births = GoatBirth.objects.filter(date__date=timezone.now().date())
    total_kidding = today_goat_births.aggregate(Sum('kiddings_num'))['kiddings_num__sum'] or 0
    # cow mortality monthly
    cow_month_mot = CowMortality.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num') + F('calves')))
    # cow procurement monthly
    cow_month_proc = CowProcurement.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num')))
    # cow culling monthly
    cow_month_cull = CowCulling.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num')))
    # calving monthly
    cow_month_birth = CowBirth.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('clavings_num')))
    # pig mortality monthly
    pig_month_mot = PigMortality.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num') + F('pigglet') + F('nursing_num') + F('hogs_num') + F('growers_num') + F('weaners_num') + F('drysows_num')))
    # pig procurement monthly
    pig_month_proc = PigProcurement.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num')))
    # pig culling monthly
    pig_month_cull = PigCulling.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num')))
    # farrowing monthly
    pig_month_birth = PigBirth.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('farrowing_num')))
    # sheep mortality monthly
    sheep_month_mot = SheepMortality.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num') + F('lamb')))
    # sheep procurement monthly
    sheep_month_proc = SheepProcurement.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num')))
    # sheep culling monthly
    sheep_month_cull = SheepCulling.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num')))
    # lambing monthly
    sheep_month_birth = SheepBirth.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('lambings_num')))
    # goat mortality monthly
    goat_month_mot = GoatMortality.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num') + F('kid')))
    # goat procurement monthly
    goat_month_proc = GoatProcurement.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num')))
    # goat culling monthly
    goat_month_cull = GoatCulling.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num')))
    # kidding monthly
    goat_month_birth = GoatBirth.objects.filter(date__month=current_month).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('kiddings_num')))

    context ={
        'current_datetime' : current_datetime,
        'ctotal' : cowpop,
        'ptotal' : pigpop,
        'stotal' : sheeppop,
        'gtotal' : goatpop,
        'workers' : section,
        'sec' : worker,
        'total_cattle_mortality': total_cattle_mortality,
        'total_cattle_procurements' : total_cattle_procurements,
        'total_clavings' : total_clavings,
        'total_cow_cull' : total_cow_cull,
        'total_pig_mortality' : total_pig_mortality,
        'total_pig_cull' : total_pig_cull,
        'total_pig_proc' : total_pig_proc,
        'total_farrowing' : total_farrowing,
        'total_sheep_mot' : total_sheep_mot,
        'total_sheep_cull' : total_sheep_cull,
        'total_sheep_proc' : total_sheep_proc,
        'total_lambing' : total_lambing,
        'total_goat_mot' : total_goat_mot,
        'total_goat_cull' : total_goat_cull,
        'total_kidding' : total_kidding,
        'total_goat_proc' : total_goat_proc,
        'cow_month_mot' : cow_month_mot,
        'cow_month_proc' : cow_month_proc,
        'cow_month_cull' : cow_month_cull,
        'cow_month_birth' : cow_month_birth,
        'pig_month_mot' : pig_month_mot,
        'pig_month_proc' : pig_month_proc,
        'pig_month_cull' : pig_month_cull,
        'pig_month_birth' : pig_month_birth,
        'sheep_month_mot' : sheep_month_mot,
        'sheep_month_proc' : sheep_month_proc,
        'sheep_month_cull' : sheep_month_cull,
        'sheep_month_birth' : sheep_month_birth,
        ' goat_month_mot' :  goat_month_mot,
        'goat_month_proc' : goat_month_proc,
        'goat_month_cull' : goat_month_cull,
        'goat_month_birth' : goat_month_birth
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
        elif user is not None and user.profile.is_hr:
            login(request, user)
            return redirect('humanR:index')
        else:
            messages.error(request, 'Username OR Password is incorrect')
            return redirect('login_page')
           
    return render(request, 'main/login.html')

@staff_required(login_url="/")
@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('login_page')


@staff_required(login_url="/")
@login_required(login_url='/')
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
        'scl' : sheepcull,

    }

    return render (request, 'main/latest-rep-animal.html', context)

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
def cow_image_view(request, slug):
    aview = CowMortality.objects.get(slug=slug)
    return render(request, 'main/cowmot-aview.html', {'cmview':aview})

@staff_required(login_url="/")
@login_required(login_url='/')
def goat_image_view(request, slug):
    aview = GoatMortality.objects.get(slug=slug)
    return render(request, 'main/goatmot-aview.html', {'gmview':aview})

@staff_required(login_url="/")
@login_required(login_url='/')
def sheep_image_view(request, slug):
    aview = SheepMortality.objects.get(slug=slug)
    return render(request, 'main/sheepmot-aview.html', {'smview':aview})

@staff_required(login_url="/")
@login_required(login_url='/')
def pig_image_view(request, slug):
    aview = PigMortality.objects.get(slug=slug)
    return render(request, 'main/pigmot-aview.html', {'pmview':aview})


@staff_required(login_url="/")
@login_required(login_url='/')
def cow_salea(request):
    csa = CowSale.objects.order_by('-date')
    query_form = CowsaleFilter()
    admin_cs = Paginator(csa, 10)
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

@staff_required(login_url="/")
@login_required(login_url='/')
def cow_proca(request):
    cpa = CowProcurement.objects.order_by('-date')
    query_form = CowprocFilter()
    admin_cp = Paginator(cpa, 10)
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

@staff_required(login_url="/")
@login_required(login_url='/')
def cow_culla(request):
    cca = CowCulling.objects.order_by('-date')
    query_form = CowcullFilter()
    paginated_filtercc = Paginator(cca, 10)
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

@staff_required(login_url="/")
@login_required(login_url='/')
def goat_mota(request):
    gma = GoatMortality.objects.order_by('-date')
    query_form = GoatmotFilter()
    admin_gm = Paginator(gma, 1)
    page_number = request.GET.get('page', 10)
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
def cow_all(request):
    c_chart = CowMortality.objects.all()
    chart_countc = c_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num') + F('calves')))
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

@staff_required(login_url="/")
@login_required(login_url='/')
def goat_all(request):
    g_chart = GoatMortality.objects.all()
    chart_countg = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num') + F('kid')))
    buckM_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('buck_num'))
    doeM_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('doe_num'))
    kid_count = g_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('kid'))
    popadg = GoatCensusPop.objects.order_by('-date').reverse()[:12]
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

@staff_required(login_url="/")
@login_required(login_url='/')
def pig_all(request):
    p_chart = PigMortality.objects.all()
    chart_countp = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num') + F('pigglet')))
    boarM_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('boar_num'))
    sowM_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('sow_num'))
    pigglet_count = p_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('pigglet'))
    popadp = PigCensusPop.objects.order_by('-date').reverse()[:12]
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

@staff_required(login_url="/")
@login_required(login_url='/')
def sheep_all(request):
    s_chart = SheepMortality.objects.all()
    chart_counts = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num') + F('lamb')))
    ramM_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ram_num'))
    eweM_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ewe_num'))
    lamb_count = s_chart.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('lamb'))
    popads = SheepCensusPop.objects.order_by('-date').reverse()  [:12]
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
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

@staff_required(login_url="/")
@login_required(login_url='/')
def review_page(request):
    if request.method == 'POST':
        comment_form = RemarkForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, 'message sent')
            comment_form = RemarkForm()
    else:
        comment_form = RemarkForm()
    return render(request, 'main/review-form.html', {'comment' : comment_form})