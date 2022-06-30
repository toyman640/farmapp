from django.shortcuts import get_object_or_404, redirect, render
from farmrecord.forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import format_html 
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models.aggregates import Count, Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F 
import csv
from farmrecord.models import *
from notification.models import Notification
# Create your views here.

@login_required(login_url='/admin-page/login')
def index(request):
    cowmot_count = CowMortality.objects.all()
    pigmot_count =  PigMortality.objects.all()
    goatmot_count = GoatMortality.objects.all()
    sheepmot_count = SheepMortality.objects.all()
    cowcen = CowCensusPop.objects.all()
    pigcen = PigCensusPop.objects.all()
    sheepcen = SheepCensusPop.objects.all()
    goatcen = GoatCensusPop.objects.all()
    aggregated = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num') + F('calves')))
    month_pig = pigmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num') + F('pigglet')))
    month_goat = goatmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num') + F('kid')))
    month_sheep = sheepmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num') + F('lamb')))
    cowmot_amt = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('cow_num'))
    bullmot_amt = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('bull_num'))
    calfmot_amt = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('calves'))
    sowmot_amt = pigmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('sow_num'))
    boarmot_amt = pigmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('boar_num'))
    pigletmot_amt = pigmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('pigglet'))
    doemot_amt = goatmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('doe_num'))
    buckmot_amt = goatmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('buck_num'))
    kidmot_amt = goatmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('kid'))
    rammot_amt = sheepmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ram_num'))
    ewemot_amt = sheepmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('ewe_num'))
    lambmot_amt = sheepmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('lamb'))
    n = Notification.objects.filter(user=request.user, viewed=False)
    
    
    context = {
        'cowpop' : cowcen,
        'pigcen' : pigcen,
        'sheepcen' : sheepcen,
        'goatcen' : goatcen,
        'count' : aggregated,
        'countp' : month_pig,
        'counts' : month_sheep,
        'countg' : month_goat,
        'cdn' : cowmot_amt,
        'bldn' : bullmot_amt,
        'cldn' : calfmot_amt,
        'sdn' : sowmot_amt,
        'brdn' : boarmot_amt,
        'pltdn' : pigletmot_amt,
        'ddn' : doemot_amt,
        'bkdn' : buckmot_amt,
        'kdn' : kidmot_amt,
        'rdn' : rammot_amt,
        'edn' : ewemot_amt,
        'ldn' : lambmot_amt,
        'notes' : n

        
    }
    return render(request, 'index.html', context)

def test(request):
    return render(request, 'test.html')

@login_required(login_url='/admin-page/login')
def cow_motrep(request):
    if request.method == 'POST':
        cow_mot = CowmotForm(request.POST, request.FILES)
        if cow_mot.is_valid():
            cow_mot.save()
            messages.success(request, 'Entry Saved')
            cow_mot=CowmotForm()
    else:
        cow_mot = CowmotForm()
    return render(request, 'cow-motrep.html',{'cow_mot': cow_mot})

@login_required(login_url='/admin-page/login')
def cow_cull(request):
    if request.method == 'POST':
        cow_cull = CowcullForm(request.POST, request.FILES)
        if cow_cull.is_valid():
            cow_cull.save()
            messages.success(request, 'Entry Saved')
            cow_cull = CowcullForm()
    else:
        cow_cull = CowcullForm()
    return render(request, 'cow-cull.html', {'cow_cull': cow_cull})

@login_required(login_url='/admin-page/login')
def cow_proc(request):
    if request.method == 'POST':
        cow_proc = CowprocForm(request.POST, request.FILES)
        if cow_proc.is_valid():
            cow_proc.save()
            messages.success(request, 'Entry Saved')
            cow_proc = CowprocForm()
    else:
        cow_proc = CowprocForm()
    return render(request, 'cow-proc.html', {'cow_proc': cow_proc})


@login_required(login_url='/admin-page/login')
def cow_sales(request):
    if request.method == 'POST':
        cow_sale = CowsaleForm(request.POST, request.FILES)
        if cow_sale.is_valid():
            cow_sale.save()
            messages.success(request, 'Entry Saved')
            cow_sale = CowsaleForm()
    else:
        cow_sale = CowsaleForm()
    return render(request, 'cow-sale.html', {'cow_sale': cow_sale})

@login_required(login_url='/admin-page/login')
def cow_birth(request):
    if request.method == 'POST':
        cow_birth = CowBirthForm(request.POST, request.FILES)
        if cow_birth.is_valid():
            cow_birth.save()
            messages.success(request, 'Entry Saved')
            cow_birth = CowBirthForm()
    else:
        cow_birth = CowBirthForm()
    return render(request, 'cow-birth.html', {'cow_birth': cow_birth})

@login_required(login_url='/admin-page/login')
def cow_motrec(request):
    cow_rec =   CowMortality.objects.order_by('-date')
    query_form = CowmotFilter()
    paginated_filtercm = Paginator(cow_rec, 10)
    page_number = request.GET.get('page')
    cm_page_obj = paginated_filtercm.get_page(page_number)
    cowmot_count = CowMortality.objects.all()
    aggregated = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    context = {
        'cm_page_obj': cow_rec,
        'q': query_form,
        'count' : aggregated
        
    }
    context['cm_page_obj'] = cm_page_obj
    return render(request, 'cowmotrec.html',context)

@login_required(login_url='/admin-page/login')
def cow_birthrec(request):
    cow_birthrec =   CowBirth.objects.order_by('-date')
    query_form = CowbirthFilter()
    paginated_filtercb = Paginator(cow_birthrec, 10)
    page_number = request.GET.get('page')
    cb_page_obj = paginated_filtercb.get_page(page_number)
    context = {
        'cb_page_obj': cow_birthrec,
        'q': query_form,  
    }
    context['cb_page_obj'] = cb_page_obj
    return render(request, 'cowbirthrec.html',context)


@login_required(login_url='/admin-page/login')
def cow_birthrec_view(request, abt_id):
    bview = CowBirth.objects.get(id=abt_id)
    return render(request, 'cowbirthrec-view.html', {'bview':bview})

@login_required(login_url='/admin-page/login')
def cow_motrec_view(request, abt_id):
    mview = CowMortality.objects.get(id=abt_id)
    return render(request, 'cowmotrec-view.html', {'mview':mview})

@login_required(login_url='/admin-page/login')
def cow_procrec_view(request, abt_id):
    Pview = CowProcurement.objects.get(id=abt_id)
    return render(request, 'cowprocrec-view.html', {'Pview':Pview})

@login_required(login_url='/admin-page/login')
def cow_salerec_view(request, abt_id):
    Sview = CowSale.objects.get(id=abt_id)
    return render(request, 'cowsalerec-view.html', {'Sview':Sview})

@login_required(login_url='/admin-page/login')
def cow_cullrec_view(request, abt_id):
    cview = CowCulling.objects.get(id=abt_id)
    return render(request, 'cowcullrec-view.html', {'cview':cview})

@login_required(login_url='/admin-page/login')
def cow_procrec(request):
    cow_prec = CowProcurement.objects.order_by('-date')
    query_form = CowprocFilter()
    paginated_filtercp = Paginator(cow_prec, 10)
    page_number = request.GET.get('page')
    cp_page_obj = paginated_filtercp.get_page(page_number)
    context = {
        'cp_page_obj': cow_prec,
        'q'    : query_form
        
    }
    context['cm_page_obj'] = cp_page_obj
    return render(request, 'cowprocrec.html', context)

@login_required(login_url='/admin-page/login')
def cow_cullrec(request):
    cow_crec = CowCulling.objects.order_by('-date')
    query_form = CowcullFilter()
    paginated_filtercc = Paginator(cow_crec, 10)
    page_number = request.GET.get('page')
    cc_page_obj = paginated_filtercc.get_page(page_number)
    context = {
        'cc_page_obj': cow_crec,
        'q'    : query_form
        
    }
    context['cc_page_obj'] = cc_page_obj
    return render(request, 'cowcullrec.html',context)

@login_required(login_url='/admin-page/login')
def cow_salerec(request):
    cow_srec = CowSale.objects.order_by('-date')
    query_form = CowsaleFilter()
    paginated_filtercs = Paginator(cow_srec, 10)
    page_number = request.GET.get('page')
    cs_page_obj = paginated_filtercs.get_page(page_number)
    context = {
        'cs_page_obj': cow_srec,
        'q'    : query_form
        
    }
    context['cs_page_obj'] = cs_page_obj
    return render(request, 'cowsalerec.html',context)

@login_required(login_url='/admin-page/login')
def goat_birth(request):
    if request.method == 'POST':
        goat_birth = GoatBirthForm(request.POST, request.FILES)
        if goat_birth.is_valid():
            goat_birth.save()
            messages.success(request, 'Entry Saved')
            goat_birth = GoatBirthForm()
    else:
        goat_birth = GoatBirthForm()
    return render(request, 'goat-birth.html', {'goat_birth' : goat_birth})

@login_required(login_url='/admin-page/login')
def goat_cull(request):
    if request.method == 'POST':
        goat_cull = GoatcullForm(request.POST, request.FILES)
        if goat_cull.is_valid():
            goat_cull.save()
            messages.success(request, 'Entry Saved')
            goat_cull = GoatcullForm()
    else:
        goat_cull = GoatcullForm()
    return render(request, 'goat-cull.html', {'goat_cull': goat_cull})

@login_required(login_url='/admin-page/login')
def goat_motrep(request):
    if request.method == 'POST':
        goat_mot = GoatmotForm(request.POST, request.FILES)
        if goat_mot.is_valid():
            goat_mot.save()
            messages.success(request, 'Entry Saved')
            goat_mot = GoatmotForm()
    else:
        goat_mot = GoatmotForm()
    return render(request, 'goat-motrep.html',{'goat_mot': goat_mot})

@login_required(login_url='/admin-page/login')
def goat_proc(request):
    if request.method == 'POST':
        goat_proc = GoatprocForm(request.POST, request.FILES)
        if goat_proc.is_valid():
            goat_proc.save()
            messages.success(request, 'Entry Saved')
            goat_proc = GoatprocForm()
    else:
        goat_proc = GoatprocForm()
    return render(request, 'goat-proc.html', {'goat_proc': goat_proc})

@login_required(login_url='/admin-page/login')
def goat_sales(request):
    if request.method == 'POST':
        goat_sale = GoatsaleForm(request.POST, request.FILES)
        if goat_sale.is_valid():
            goat_sale.save()
            messages.success(request, 'Entry Saved')
            goat_sale = GoatsaleForm()
    else:
        goat_sale = GoatsaleForm()
    return render(request, 'goat-sale.html', {'goat_sale': goat_sale})

@login_required(login_url='/admin-page/login')
def goat_birthrec(request):
    goat_birthrec =   GoatBirth.objects.order_by('-date')
    query_form = GoatbirthFilter()
    paginated_filtergb = Paginator(goat_birthrec, 10)
    page_number = request.GET.get('page')
    gb_page_obj = paginated_filtergb.get_page(page_number)
    context = {
        'gb_page_obj': goat_birthrec,
        'q': query_form,  
    }
    context['gb_page_obj'] = gb_page_obj
    return render(request, 'goatbirthrec.html',context)



@login_required(login_url='/admin-page/login')
def goat_motrec(request):
    goat_mrec =   GoatMortality.objects.order_by('-date')
    query_form = GoatmotFilter()
    paginated_filtergm = Paginator(goat_mrec, 10)
    page_number = request.GET.get('page')
    gm_page_obj = paginated_filtergm.get_page(page_number)
    context = {
        'gm_page_obj': goat_mrec,
        'q'    : query_form
        
    }
    context['gm_page_obj'] = gm_page_obj
    return render(request, 'goatmotrec.html', context)

@login_required(login_url='/admin-page/login')
def goat_procrec(request):
    goat_prec = GoatProcurement.objects.order_by('-date')
    query_form = GoatprocFilter()
    paginated_filtergp = Paginator(goat_prec, 10)
    page_number = request.GET.get('page')
    gp_page_obj = paginated_filtergp.get_page(page_number)
    context = {
        'gp_page_obj': goat_prec,
        'q'    : query_form
        
    }
    context['gp_page_obj'] = gp_page_obj
    return render(request, 'goatprocrec.html',context)

@login_required(login_url='/admin-page/login')
def goat_cullrec(request):
    goat_crec = GoatCulling.objects.order_by('-date')
    query_form = GoatcullFilter()
    paginated_filtergc = Paginator(goat_crec, 10)
    page_number = request.GET.get('page')
    gc_page_obj = paginated_filtergc.get_page(page_number)
    context = {
        'gc_page_obj': goat_crec,
        'q'   : query_form
        
    }
    context['gc_page_obj'] = gc_page_obj
    return render(request, 'goatcullrec.html',context)

@login_required(login_url='/admin-page/login')
def goat_salerec(request):
    goat_srec = GoatSale.objects.order_by('-date')
    query_form = GoatsaleFilter()
    paginated_filtergs = Paginator(goat_srec, 10)
    page_number = request.GET.get('page')
    gs_page_obj = paginated_filtergs.get_page(page_number)
    context = {
        'gs_page_obj': goat_srec,
        'q'    : query_form
        
    }
    context['gs_page_obj'] = gs_page_obj
    return render(request, 'goatsalerec.html',context)

@login_required(login_url='/admin-page/login')
def goat_birthrec_view(request, abt_id):
    Bview = GoatBirth.objects.get(id=abt_id)
    return render(request, 'goatbirthrec-view.html', {'Bview':Bview})

@login_required(login_url='/admin-page/login')
def goat_motrec_view(request, abt_id):
    Mview = GoatMortality.objects.get(id=abt_id)
    return render(request, 'goatmotrec-view.html', {'Mview':Mview})

@login_required(login_url='/admin-page/login')
def goat_cullrec_view(request, abt_id):
    Cview = GoatCulling.objects.get(id=abt_id)
    return render(request, 'goatcullrecview.html', {'Cview':Cview})

@login_required(login_url='/admin-page/login')
def goat_salerec_view(request, abt_id):
    Sview = GoatSale.objects.get(id=abt_id)
    return render(request, 'goatsalerec-view.html', {'Sview':Sview})

@login_required(login_url='/admin-page/login')
def goat_procrec_view(request, abt_id):
    Pview = GoatProcurement.objects.get(id=abt_id)
    return render(request, 'goatprocrec-view.html', {'Pview':Pview})

@login_required(login_url='/admin-page/login')
def pig_sales(request):
    if request.method == 'POST':
        pig_sale = PigsaleForm(request.POST, request.FILES)
        if pig_sale.is_valid():
            pig_sale.save()
            messages.success(request, 'Entry Saved')
            pig_sale = PigsaleForm()
    else:
        pig_sale = PigsaleForm()
    return render(request, 'pig-sales.html', {'pig_sale': pig_sale})

@login_required(login_url='/admin-page/login')
def pig_birth(request):
    if request.method == 'POST':
        pig_birth = PigBirthForm(request.POST, request.FILES)
        if pig_birth.is_valid():
            pig_birth.save()
            messages.success(request, 'Entry Saved')
            pig_birth = PigBirthForm()
    else:
        pig_birth = PigBirthForm()
    return render(request, 'pig-birth.html', {'pig_birth' : pig_birth})

@login_required(login_url='/admin-page/login')
def pig_cull(request):
    if request.method == 'POST':
        pig_cull = PigcullForm(request.POST, request.FILES)
        if pig_cull.is_valid():
            pig_cull.save()
            messages.success(request, 'Entry Saved')
            pig_cull = PigcullForm()
    else:
        pig_cull = PigcullForm()
    return render(request, 'pig-cull.html', {'pig_cull': pig_cull})

@login_required(login_url='/admin-page/login')
def pig_motrep(request):
    if request.method == 'POST':
        pig_mot = PigmotForm(request.POST, request.FILES)
        if pig_mot.is_valid():
            pig_mot.save()
            messages.success(request, 'Entry Saved')
            pig_mot = PigmotForm()
    else:
        pig_mot = PigmotForm()
    return render(request, 'pig-motrep.html',{'pig_mot': pig_mot})

@login_required(login_url='/admin-page/login')
def pig_proc(request):
    if request.method == 'POST':
        pig_proc = PigprocForm(request.POST, request.FILES)
        if pig_proc.is_valid():
            pig_proc.save()
            messages.success(request, 'Entry Saved')
            pig_proc = PigprocForm()
    else:
        pig_proc = PigprocForm()
    return render(request, 'pig-proc.html', {'pig_proc': pig_proc})

@login_required(login_url='/admin-page/login')
def pig_birthrec(request):
    pig_birthrec =   PigBirth.objects.order_by('-date')
    query_form = PigbirthFilter()
    paginated_filterpb = Paginator(pig_birthrec, 10)
    page_number = request.GET.get('page')
    pb_page_obj = paginated_filterpb.get_page(page_number)
    context = {
        'pb_page_obj': pig_birthrec,
        'q': query_form,  
    }
    context['pb_page_obj'] = pb_page_obj
    return render(request, 'pigbirthrec.html',context)


@login_required(login_url='/admin-page/login')
def pig_motrec(request):
    pig_mrec =   PigMortality.objects.order_by('-date')
    query_form = PigmotFilter()
    paginated_filterpm = Paginator(pig_mrec, 10)
    page_number = request.GET.get('page')
    pm_page_obj = paginated_filterpm.get_page(page_number)
    context = {
        'pm_page_obj': pig_mrec,
        'q'    : query_form
        
    }
    context['pm_page_obj'] = pm_page_obj
    return render(request, 'pigmotrec.html', context)

@login_required(login_url='/admin-page/login')
def pig_procrec(request):
    pig_prec = PigProcurement.objects.order_by('-date')
    query_form = PigprocFilter()
    paginated_filterpp = Paginator(pig_prec, 10)
    page_number = request.GET.get('page')
    pp_page_obj = paginated_filterpp.get_page(page_number)
    context = {
        'pp_page_obj': pig_prec,
        'q'    : query_form
        
    }
    context['pp_page_obj'] = pp_page_obj
    return render(request, 'pigprocrec.html', context)

@login_required(login_url='/admin-page/login')    
def pig_salerec(request):
    pig_srec = PigSale.objects.order_by('-date')
    query_form = PigsaleFilter()
    paginated_filterps = Paginator(pig_srec, 10)
    page_number = request.GET.get('page')
    ps_page_obj = paginated_filterps.get_page(page_number)
    context = {
        'ps_page_obj': pig_srec,
        'q'    : query_form
        
    }
    context['ps_page_obj'] = ps_page_obj
    return render(request, 'pigsalerec.html',context)

@login_required(login_url='/admin-page/login')
def pig_cullrec(request):
    pig_crec = PigCulling.objects.order_by('-date')
    query_form = PigcullFilter() 
    paginated_filterpc = Paginator(pig_crec, 10)
    page_number = request.GET.get('page')
    pc_page_obj = paginated_filterpc.get_page(page_number)
    context = {
        'pc_page_obj': pig_crec,
        'q'    : query_form
        
    }
    context['pc_page_obj'] = pc_page_obj
    return render(request, 'pigcullrec.html', context)


@login_required(login_url='/admin-page/login')
def pig_birthrec_view(request, abt_id):
    Bview = PigBirth.objects.get(id=abt_id)
    return render(request, 'pigbirthrec-view.html', {'Bview':Bview})

@login_required(login_url='/admin-page/login')
def pig_procrec_view(request, abt_id):
    Pview = PigProcurement.objects.get(id=abt_id)
    return render(request, 'pigprocrec-view.html', {'Pview':Pview})

@login_required(login_url='/admin-page/login')
def pig_motrec_view(request, abt_id):
    Mview = PigMortality.objects.get(id=abt_id)
    return render(request, 'pigmotrec-view.html', {'Mview':Mview})

@login_required(login_url='/admin-page/login')
def pig_salerec_view(request, abt_id):
    Sview = PigSale.objects.get(id=abt_id)
    return render(request, 'pigsalerecview.html', {'Sview':Sview})

@login_required(login_url='/admin-page/login')
def pig_cullrec_view(request, abt_id):
    Cview = PigCulling.objects.get(id=abt_id)
    return render(request, 'pigcullrecview.html', {'Cview':Cview})

@login_required(login_url='/admin-page/login')
def sheep_birth(request):
    if request.method == 'POST':
        sheep_birth = SheepBirthForm(request.POST, request.FILES)
        if sheep_birth.is_valid():
            sheep_birth.save()
            messages.success(request, 'Entry Saved')
            sheep_birth = SheepBirthForm()
    else:
        sheep_birth = SheepBirthForm()
    return render(request, 'sheep-birth.html', {'sheep_birth' : sheep_birth})

@login_required(login_url='/admin-page/login')
def sheep_cull(request):
    if request.method == 'POST':
        sheep_cull = SheepcullForm(request.POST, request.FILES)
        if sheep_cull.is_valid():
            sheep_cull.save()
            messages.success(request, 'Entry Saved')
            sheep_cull = SheepcullForm()
    else:
        sheep_cull = SheepcullForm()
    return render(request, 'sheep-cull.html', {'sheep_cull': sheep_cull})

@login_required(login_url='/admin-page/login')
def sheep_motrep(request):
    if request.method == 'POST':
        sheep_mot = SheepmotForm(request.POST, request.FILES)
        if sheep_mot.is_valid():
            sheep_mot.save()
            messages.success(request, 'Entry Saved')
            sheep_mot = SheepmotForm()
    else:
        sheep_mot = SheepmotForm()
    return render(request, 'sheep-mot.html',{'sheep_mot': sheep_mot})

@login_required(login_url='/admin-page/login')
def sheep_proc(request):
    if request.method == 'POST':
        sheep_proc = SheepprocForm(request.POST, request.FILES)
        if sheep_proc.is_valid():
            sheep_proc.save()
            messages.success(request, 'Entry Saved')
            sheep_proc = SheepprocForm()
    else:
        sheep_proc = SheepprocForm()
    return render(request, 'sheep-proc.html', {'sheep_proc': sheep_proc})

@login_required(login_url='/admin-page/login')
def sheep_sales(request):
    if request.method == 'POST':
        sheep_sale = SheepsaleForm(request.POST, request.FILES)
        if sheep_sale.is_valid():
            sheep_sale.save()
            messages.success(request, 'Entry Saved')
            sheep_sale = SheepsaleForm()
    else:
        sheep_sale = SheepsaleForm()
    return render(request, 'sheep-sales.html', {'sheep_sale': sheep_sale})

@login_required(login_url='/admin-page/login')
def sheep_birthrec(request):
    sheep_birthrec =   SheepBirth.objects.order_by('-date')
    query_form = SheepbirthFilter()
    paginated_filtersb = Paginator(sheep_birthrec, 10)
    page_number = request.GET.get('page')
    sb_page_obj = paginated_filtersb.get_page(page_number)
    context = {
        'sb_page_obj': sheep_birthrec,
        'q': query_form,  
    }
    context['sb_page_obj'] = sb_page_obj
    return render(request, 'sheepbirthrec.html',context)



@login_required(login_url='/admin-page/login')
def sheep_motrec(request):
    sheep_mrec = SheepMortality.objects.order_by('-date')
    query_form = SheepmotFilter() 
    paginated_filtersm = Paginator(sheep_mrec, 10)
    page_number = request.GET.get('page')
    sm_page_obj = paginated_filtersm.get_page(page_number)
    context = {
        'sm_page_obj': sheep_mrec,
        'q'   : query_form
        
    }
    context['sm_page_obj'] = sm_page_obj
    return render(request, 'sheepmotrec.html',context)

@login_required(login_url='/admin-page/login')
def sheep_procrec(request):
    sheep_prec = SheepProcurement.objects.order_by('-date')
    query_form = SheepprocFilter()
    paginated_filtersp = Paginator(sheep_prec, 10)
    page_number = request.GET.get('page')
    sp_page_obj = paginated_filtersp.get_page(page_number)
    context = {
        'sp_page_obj': sheep_prec,
        'q'    : query_form
        
    }
    context['sp_page_obj'] = sp_page_obj
    return render(request, 'sheepprocrec.html',context)

@login_required(login_url='/admin-page/login')
def sheep_cullrec(request):
    sheep_crec = SheepCulling.objects.order_by('-date')
    query_form = SheepcullFilter()
    paginated_filtersc = Paginator(sheep_crec, 10)
    page_number = request.GET.get('page')
    sc_page_obj = paginated_filtersc.get_page(page_number)
    context = {
        'sc_page_obj': sheep_crec,
        'q'    : query_form
        
    }
    context['sc_page_obj'] = sc_page_obj
    return render(request, 'sheepcullrec.html',context)

@login_required(login_url='/admin-page/login')
def sheep_salerec(request):
    sheep_srec = SheepSale.objects.order_by('-date')
    query_form = SheepsaleFilter() 
    paginated_filterss = Paginator(sheep_srec, 10)
    page_number = request.GET.get('page')
    ss_page_obj = paginated_filterss.get_page(page_number)
    context = {
        'ss_page_obj': sheep_srec,
        'q'    : query_form
        
    }
    context['ss_page_obj'] = ss_page_obj
    return render(request, 'sheepsalerec.html',context)


@login_required(login_url='/admin-page/login')
def sheep_birthrec_view(request, abt_id):
    Bview = SheepBirth.objects.get(id=abt_id)
    return render(request, 'sheepbirthrec-view.html', {'Bview':Bview})

@login_required(login_url='/admin-page/login')
def sheep_motrec_view(request, abt_id):
    Mview = SheepMortality.objects.get(id=abt_id)
    return render(request, 'sheepmotrec-view.html', {'Mview':Mview})

@login_required(login_url='/admin-page/login')
def sheep_procrec_view(request, abt_id):
    Pview = SheepProcurement.objects.get(id=abt_id)
    return render(request, 'sheepprocrec-view.html', {'Pview':Pview})

@login_required(login_url='/admin-page/login')
def sheep_salerec_view(request, abt_id):
    Sview = SheepSale.objects.get(id=abt_id)
    return render(request, 'sheepsalerec-view.html', {'Sview':Sview})

@login_required(login_url='/admin-page/login')
def sheep_cullrec_view(request, abt_id):
    Cview = SheepCulling.objects.get(id=abt_id)
    return render(request, 'sheepcullrec-view.html', {'Cview':Cview})

@login_required(login_url='/admin-page/login')
def delete_postc(request, listf_id):
    post_record = get_object_or_404(CowMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:cow_motrec')

@login_required(login_url='/admin-page/login')
def delete_postg(request, listg_id):
    post_record = get_object_or_404(GoatMortality, id=listg_id)
    post_record.delete()
    return redirect('farmrecord:goat_motrec')

@login_required(login_url='/admin-page/login')
def delete_posts(request, listf_id):
    post_record = get_object_or_404(SheepMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:sheep_motrec')

@login_required(login_url='/admin-page/login')
def delete_postp(request, listf_id):
    post_record = get_object_or_404(PigMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:pig_motrec')

@login_required(login_url='/admin-page/login')
def delete_postcullg(request, listcullg_id):
    post_record = get_object_or_404(GoatCulling, id=listcullg_id)
    post_record.delete()
    return redirect('farmrecord:goat_cullrec')

@login_required(login_url='/admin-page/login')
def delete_postcullp(request, listcullp_id):
    post_record = get_object_or_404(PigCulling, id=listcullp_id)
    post_record.delete()
    return redirect('farmrecord:pig_cullrec')

@login_required(login_url='/admin-page/login')
def delete_postbirths(request, listbirths_id):
    post_record = get_object_or_404(SheepBirth, id=listbirths_id)
    post_record.delete()
    return redirect('farmrecord:sheep_birthrec')


@login_required(login_url='/admin-page/login')
def delete_postculls(request, listculls_id):
    post_record = get_object_or_404(SheepCulling, id=listculls_id)
    post_record.delete()
    return redirect('farmrecord:sheep_cullrec')

@login_required(login_url='/admin-page/login')
def delete_postbirthc(request, listbirthc_id):
    post_record = get_object_or_404(CowBirth, id=listbirthc_id)
    post_record.delete()
    return redirect('farmrecord:cow_birthrec')

@login_required(login_url='/admin-page/login')
def delete_postcullc(request, listcullc_id):
    post_record = get_object_or_404(CowCulling, id=listcullc_id)
    post_record.delete()
    return redirect('farmrecord:cow_cullrec')

@login_required(login_url='/admin-page/login')
def delete_postsalec(request, listsalec_id):
    post_record = get_object_or_404(CowSale, id=listsalec_id)
    post_record.delete()
    return redirect('farmrecord:cow_salerec')

@login_required(login_url='/admin-page/login')
def delete_postbirthg(request, listbirthg_id):
    post_record = get_object_or_404(GoatBirth, id=listbirthg_id)
    post_record.delete()
    return redirect('farmrecord:goat_birthrec')

@login_required(login_url='/admin-page/login')
def delete_postsaleg(request, listsaleg_id):
    post_record = get_object_or_404(GoatSale, id=listsaleg_id)
    post_record.delete()
    return redirect('farmrecord:goat_salerec')

@login_required(login_url='/admin-page/login')
def delete_postbirthp(request, listbirthp_id):
    post_record = get_object_or_404(PigBirth, id=listbirthp_id)
    post_record.delete()
    return redirect('farmrecord:pig_birthrec')


@login_required(login_url='/admin-page/login')
def delete_postsalep(request, listsalep_id):
    post_record = get_object_or_404(PigSale, id=listsalep_id)
    post_record.delete()
    return redirect('farmrecord:pig_salerec')

@login_required(login_url='/admin-page/login')
def delete_postsales(request, listsales_id):
    post_record = get_object_or_404(SheepSale, id=listsales_id)
    post_record.delete()
    return redirect('farmrecord:sheep_salerec')

@login_required(login_url='/admin-page/login')
def delete_postprocc(request, listprocc_id):
    post_record = get_object_or_404(CowProcurement, id=listprocc_id)
    post_record.delete()
    return redirect('farmrecord:cow_procrec')

@login_required(login_url='/admin-page/login')
def delete_postprocg(request, listprocg_id):
    post_record = get_object_or_404(GoatProcurement, id=listprocg_id)
    post_record.delete()
    return redirect('farmrecord:goat_procrec')

@login_required(login_url='/admin-page/login')
def delete_postprocp(request, listprocp_id):
    post_record = get_object_or_404(PigProcurement, id=listprocp_id)
    post_record.delete()
    return redirect('farmrecord:pig_procrec')

@login_required(login_url='/admin-page/login')
def delete_postprocs(request, listprocs_id):
    post_record = get_object_or_404(SheepProcurement, id=listprocs_id)
    post_record.delete()
    return redirect('farmrecord:sheep_procrec')

@login_required(login_url='/admin-page/login')
def edit_cowmot(request, post_id):
    single_log = get_object_or_404(CowMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/cow-motality-records">click here to go back </a>'))
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Ecowmot.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_goatmot(request, post_id):
    single_log = get_object_or_404(GoatMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/goat-mortality-records">click here to go back</a>'))
    else:
        edit_motc = EditgoatMot(instance=single_log)
    return render(request, 'Egoatmot.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_sheepmot(request, post_id):
    single_log = get_object_or_404(SheepMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/sheep-mortality-records">click here to go back</a>'))
    else:
        edit_motc = EditsheepMot(instance=single_log)
    return render(request, 'Esheepmot.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_pigmot(request, post_id):
    single_log = get_object_or_404(PigMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/pig-mortality-records">click here to go back</a>'))
    else:
        edit_motc = EditpigMot(instance=single_log)
    return render(request, 'Epigmot.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_cowsale(request, post_id):
    single_log = get_object_or_404(CowSale, id=post_id)
    if request.method == 'POST':
        edit_salec = EditcowSale(request.POST, request.FILES, instance=single_log)
        if edit_salec.is_valid():
            edit_salec.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/cow-sale-records">click here to go back</a>'))
    else:
        edit_salec = EditcowSale(instance=single_log)
    return render(request, 'Ecowsale.html', {'edit_keycs': edit_salec})


@login_required(login_url='/admin-page/login')
def edit_goatsale(request, post_id):
    single_log = get_object_or_404(GoatSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/goat-sale-records">click here to go back</a>'))
    else:
        edit_motc = EditgoatSale(instance=single_log)
    return render(request, 'Egoatsale.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_pigsale(request, post_id):
    single_log = get_object_or_404(PigSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/pig-sale-records">click here to go back</a>'))
    else:
        edit_motc = EditpigSale(instance=single_log)
    return render(request, 'Epigsale.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_sheepsale(request, post_id):
    single_log = get_object_or_404(SheepSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/sheep-sale-records">click here to go back</a>'))
    else:
        edit_motc = EditsheepSale(instance=single_log)
    return render(request, 'Esheepsale.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_cowproc(request, post_id):
    single_log = get_object_or_404(CowProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowProc(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/cow-procurement-records">click here to go back</a>'))
    else:
        edit_motc = EditcowProc(instance=single_log)
    return render(request, 'Ecowproc.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_goatproc(request, post_id):
    single_log = get_object_or_404(GoatProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatProc(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/goat-procurement-records">click here to go back</a>'))
    else:
        edit_motc = EditgoatProc(instance=single_log)
    return render(request, 'Egoatproc.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_pigproc(request, post_id):
    single_log = get_object_or_404(PigProcurement, id=post_id)
    if request.method == 'POST':
        edit_procp = EditpigProc(request.POST, request.FILES, instance=single_log)
        if edit_procp.is_valid():
            edit_procp.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/pig-procurement-records">click here to go back</a>'))
    else:
        edit_procp = EditpigProc(instance=single_log)
    return render(request, 'Epigproc.html', {'edit_procp': edit_procp})

@login_required(login_url='/admin-page/login')
def edit_sheepproc(request, post_id):
    single_log = get_object_or_404(SheepProcurement, id=post_id)
    if request.method == 'POST':
        edit_procs = EditsheepProc(request.POST, request.FILES, instance=single_log)
        if edit_procs.is_valid():
            edit_procs.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/sheep-procurement-records">click here to go back</a>'))
    else:
        edit_procs = EditsheepProc(instance=single_log)
    return render(request, 'Esheepproc.html', {'edit_keycm': edit_procs})

@login_required(login_url='/admin-page/login')
def edit_cowcull(request, post_id):
    single_log = get_object_or_404(CowCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/cow-cull-records">click here to go back</a>'))
    else:
        edit_motc = EditcowCull(instance=single_log)
    return render(request, 'Ecowcull.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_goatcull(request, post_id):
    single_log = get_object_or_404(GoatCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/goat-cull-records">click here to go back</a>'))
    else:
        edit_motc = EditgoatCull(instance=single_log)
    return render(request, 'Egoatcull.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_sheepcull(request, post_id):
    single_log = get_object_or_404(SheepCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/sheep-cull-records">click here to go back/a>'))
    else:
        edit_motc = EditsheepCull(instance=single_log)
    return render(request, 'Esheepcull.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def edit_pigcull(request, post_id):
    single_log = get_object_or_404(PigCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully,<a href="/pages/pig-cull-records">click here to go back</a>'))
    else:
        edit_motc = EditpigCull(instance=single_log)
    return render(request, 'Epigcull.html', {'edit_keycm': edit_motc})

@login_required(login_url='/admin-page/login')
def cowmot_filter(request):
    if request.method == 'GET':
        cowmot_query = CowmotFilter(request.GET)
        if cowmot_query.is_valid():
            start_date = cowmot_query.cleaned_data.get('start_date')
            end_date = cowmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowMortality.objects.filter(date__range=[start_date, new_end])
            if cowmot_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Cow-Mortality-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Location(s)', 'Cow Num', 'Bull Num', 'Calf num', 'Cause of Mortality'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.location, row.cow_num, row.bull_num, row.calves, row.comment])
                return response
            return render(request, 'filter-cowmot.html', {'queryset': result, 'q': cowmot_query})
            
        else:
            messages.error(request, 'Out of range')
    else:
        cowmot_query = CowmotFilter()
    return render(request, 'filter-cowmot.html', {'q': cowmot_query})

@login_required(login_url='/admin-page/login')
def goatmot_filter(request):
    if request.method == 'GET':
        goatmot_query = GoatmotFilter(request.GET)
        if goatmot_query.is_valid():
            start_date = goatmot_query.cleaned_data.get('start_date')
            end_date = goatmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatMortality.objects.filter(date__range=[start_date, new_end])
            if goatmot_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Goat-Mortality-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Location(s)', 'Doe Num', 'Buck Num', 'Kid num', 'Cause of Mortality'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.location, row.doe_num, row.buck_num, row.kid, row.comment])
                return response
            return render(request, 'filter-goatmot.html', {'queryset': result, 'q': goatmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatmot_query = GoatmotFilter()
    return render(request, 'filter-goatmot.html', {'q': goatmot_query})

@login_required(login_url='/admin-page/login')
def pigmot_filter(request):
    if request.method == 'GET':
        pigmot_query = PigmotFilter(request.GET)
        if pigmot_query.is_valid():
            start_date = pigmot_query.cleaned_data.get('start_date')
            end_date = pigmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigMortality.objects.filter(date__range=[start_date, new_end])
            if pigmot_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Pig-Mortality-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Location(s)', 'Sow Num', 'Boar Num', 'Pigglet num', 'Cause of Mortality'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.location, row.sow_num, row.boar_num, row.pigglet, row.comment])
                return response
            return render(request, 'filter-pigmot.html', {'queryset': result, 'q': pigmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigmot_query = PigmotFilter()
    return render(request, 'filter-pigmot.html', {'q': pigmot_query})

@login_required(login_url='/admin-page/login')
def sheepmot_filter(request):
    if request.method == 'GET':
        sheepmot_query = SheepmotFilter(request.GET)
        if sheepmot_query.is_valid():
            start_date = sheepmot_query.cleaned_data.get('start_date')
            end_date = sheepmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepMortality.objects.filter(date__range=[start_date, new_end])
            if sheepmot_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Sheep-Mortality-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Location(s)', 'Ewe Num', 'Ram Num', 'lamb num', 'Cause of Mortality'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.location, row.ewe_num, row.ram_num, row.lamb, row.comment])
                return response
            return render(request, 'filter-sheepmot.html', {'queryset': result, 'q': sheepmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepmot_query = SheepmotFilter()
    return render(request, 'filter-sheepmot.html', {'q': sheepmot_query})

@login_required(login_url='/admin-page/login')
def sheepsale_filter(request):
    if request.method == 'GET':
        sheepsale_query = SheepsaleFilter(request.GET)
        if sheepsale_query.is_valid():
            start_date = sheepsale_query.cleaned_data.get('start_date')
            end_date = sheepsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepSale.objects.filter(date__range=[start_date, new_end])
            if sheepsale_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Sheep-sale-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Ewe Num','Size','Price', 'Ram Num','Size','Price',  'Weight(s)', 'Total Price'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.ewe_num, row.size, row.price, row.ram_num, row.size1, row.price1, row.weight, row.total_price])
                return response
            return render(request, 'filter-sheepsale.html', {'queryset': result, 'q': sheepsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepsale_query = SheepsaleFilter()
    return render(request, 'filter-sheepsale.html', {'q': sheepsale_query})

@login_required(login_url='/admin-page/login')
def pigsale_filter(request):
    if request.method == 'GET':
        pigsale_query = PigsaleFilter(request.GET)
        if pigsale_query.is_valid():
            start_date = pigsale_query.cleaned_data.get('start_date')
            end_date = pigsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigSale.objects.filter(date__range=[start_date, new_end])
            if pigsale_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Pig-sale-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Sow Num','Size','Price', 'Boar Num','Size','Price',  'Weight(s)', 'Total Price'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.sow_num, row.size, row.price, row.boar_num, row.size1, row.price1, row.weight, row.total_price])
                return response
            return render(request, 'filter-pigsale.html', {'queryset': result, 'q': pigsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigsale_query = PigsaleFilter()
    return render(request, 'filter-pigsale.html', {'q': pigsale_query})

@login_required(login_url='/admin-page/login')
def cowsale_filter(request):
    if request.method == 'GET':
        cowsale_query = CowsaleFilter(request.GET)
        if cowsale_query.is_valid():
            start_date = cowsale_query.cleaned_data.get('start_date')
            end_date = cowsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowSale.objects.filter(date__range=[start_date, new_end])
            if cowsale_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Cow-sale-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Cow Num','Size','Price', 'Bull Num','Size','Price',  'Weight(s)', 'Total Price'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.cow_num, row.size, row.price, row.bull_num, row.size1, row.price1, row.weight, row.total_price])
                return response
            return render(request, 'filter-cowsale.html', {'queryset': result, 'q': cowsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowsale_query = CowsaleFilter()
    return render(request, 'filter-cowsale.html', {'q': cowsale_query})

@login_required(login_url='/admin-page/login')
def goatsale_filter(request):
    if request.method == 'GET':
        goatsale_query = GoatsaleFilter(request.GET)
        if goatsale_query.is_valid():
            start_date = goatsale_query.cleaned_data.get('start_date')
            end_date = goatsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatSale.objects.filter(date__range=[start_date, new_end])
            if goatsale_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Goat-sale-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Doe Num','Size','Price', 'Buck Num','Size','Price',  'Weight(s)', 'Total Price'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.doe_num, row.size, row.price, row.buck_num, row.size1, row.price1, row.weight, row.total_price])
                return response
            return render(request, 'filter-sheepsale.html', {'queryset': result, 'q': goatsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatsale_query = GoatsaleFilter()
    return render(request, 'filter-sheepsale.html', {'q': goatsale_query})

@login_required(login_url='/admin-page/login')
def sheepproc_filter(request):
    if request.method == 'GET':
        sheepproc_query = SheepprocFilter(request.GET)
        if sheepproc_query.is_valid():
            start_date = sheepproc_query.cleaned_data.get('start_date')
            end_date = sheepproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepProcurement.objects.filter(date__range=[start_date, new_end])
            if sheepproc_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Sheep-procurement-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Ewe Num', 'Size', 'Ram Num','Size'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.ewe_num, row.size, row.ram_num, row.size1])
                return response
            return render(request, 'filter-sheepproc.html', {'queryset': result, 'q': sheepproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepproc_query = SheepprocFilter()
    return render(request, 'filter-sheepproc.html', {'q': sheepproc_query})

@login_required(login_url='/admin-page/login')
def pigproc_filter(request):
    if request.method == 'GET':
        pigproc_query = PigprocFilter(request.GET)
        if pigproc_query.is_valid():
            start_date = pigproc_query.cleaned_data.get('start_date')
            end_date = pigproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigProcurement.objects.filter(date__range=[start_date, new_end])
            if pigproc_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Pig-procurement-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Sow Num', 'Size', 'Boar Num','Size'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.sow_num, row.size, row.boar_num, row.size1])
                return response
            return render(request, 'filter-pigproc.html', {'queryset': result, 'q': pigproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigproc_query = PigprocFilter()
    return render(request, 'filter-pigproc.html', {'q': pigproc_query})

@login_required(login_url='/admin-page/login')
def cowproc_filter(request):
    if request.method == 'GET':
        cowproc_query = CowprocFilter(request.GET)
        if cowproc_query.is_valid():
            start_date = cowproc_query.cleaned_data.get('start_date')
            end_date = cowproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowProcurement.objects.filter(date__range=[start_date, new_end])
            if cowproc_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Cow-procurement-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Cow Num', 'Size', 'Bull Num','Size'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.cow_num, row.size, row.bull_num, row.size1])
                return response
            return render(request, 'filter-cowproc.html', {'queryset': result, 'q': cowproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowproc_query = CowprocFilter()
    return render(request, 'filter-sheepproc.html', {'q': cowproc_query})

@login_required(login_url='/admin-page/login')
def goatproc_filter(request):
    if request.method == 'GET':
        goatproc_query = GoatprocFilter(request.GET)
        if goatproc_query.is_valid():
            start_date = goatproc_query.cleaned_data.get('start_date')
            end_date = goatproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatProcurement.objects.filter(date__range=[start_date, new_end])
            if goatproc_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Goat-procurement-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Doe Num', 'Size', 'Buck Num','Size'])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.doe_num, row.size, row.buck_num, row.size1])
                return response
            return render(request, 'filter-goatproc.html', {'queryset': result, 'q': goatproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatproc_query = GoatprocFilter()
    return render(request, 'filter-goatproc.html', {'q': goatproc_query})

@login_required(login_url='/admin-page/login')
def cowcull_filter(request):
    if request.method == 'GET':
        cowcull_query = CowcullFilter(request.GET)
        if cowcull_query.is_valid():
            start_date = cowcull_query.cleaned_data.get('start_date')
            end_date = cowcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowCulling.objects.filter(date__range=[start_date, new_end])
            if cowcull_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Cow-Cull-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Cow Num', 'Bull Num','Location(s)', 'Reason',])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.cow_num,  row.bull_num, row.location, row.reason])
                return response
            return render(request, 'filter-cowcull.html', {'queryset': result, 'b': cowcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowcull_query = CowcullFilter()
    return render(request, 'filter-cowcull.html', {'b': cowcull_query})


@login_required(login_url='/admin-page/login')
def goatcull_filter(request):
    if request.method == 'GET':
        goatcull_query = GoatcullFilter(request.GET)
        if goatcull_query.is_valid():
            start_date = goatcull_query.cleaned_data.get('start_date')
            end_date = goatcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatCulling.objects.filter(date__range=[start_date, new_end])
            if goatcull_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Goat-Cull-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Doe Num', 'Buck Num','Location(s)', 'Reason',])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.doe_num,  row.buck_num, row.location, row.reason])
                return response
            return render(request, 'filter-goatcull.html', {'queryset': result, 'q': goatcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatcull_query = GoatcullFilter()
    return render(request, 'filter-goatcull.html', {'q': goatcull_query})

@login_required(login_url='/admin-page/login')
def sheepcull_filter(request):
    if request.method == 'GET':
        sheepcull_query = SheepcullFilter(request.GET)
        if sheepcull_query.is_valid():
            start_date = sheepcull_query.cleaned_data.get('start_date')
            end_date = sheepcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepCulling.objects.filter(date__range=[start_date, new_end])
            if sheepcull_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Sheep-cull-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Ewe Num', 'Ram Num','Location(s)', 'Reason',])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.ewe_num,  row.ram_num, row.location, row.reason])
                return response
            return render(request, 'filter-sheepcull.html', {'queryset': result, 'q': sheepcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepcull_query = SheepcullFilter()
    return render(request, 'filter-sheepcull.html', {'q': sheepcull_query})

@login_required(login_url='/admin-page/login')
def pigcull_filter(request):
    if request.method == 'GET':
        pigcull_query = PigcullFilter(request.GET)
        if pigcull_query.is_valid():
            start_date = pigcull_query.cleaned_data.get('start_date')
            end_date = pigcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigCulling.objects.filter(date__range=[start_date, new_end])
            if pigcull_query['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Pig-cull-Records.csv"'
                writer = csv.writer(response)
                writer.writerow(['Date', 'Sow Num', 'Boar Num','Location(s)', 'Reason',])
                instance = result
                for row in instance:
                    writer.writerow([row.date, row.sow_num,  row.boar_num, row.location, row.reason])
                return response
            return render(request, 'filter-pigcull.html', {'queryset': result, 'q': pigcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigcull_query = PigcullFilter()
    return render(request, 'filter-pigcull.html', {'q': pigcull_query})
    
@login_required(login_url='/admin-page/login')
def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='/admin-page/login')
def cen_cow(request):
    if request.method == 'POST':
        cow_cen = CowCen(request.POST, request.FILES)
        if cow_cen.is_valid():
            cow_cen.save()
            messages.success(request, 'Entry Saved')
            cow_cen = CowCen()
    else:
        cow_cen = CowCen()
    return render(request, 'cow-cen.html', {'cow_cen': cow_cen})

@login_required(login_url='/admin-page/login')
def cen_goat(request):
    if request.method == 'POST':
        goat_cen = GoatCen(request.POST, request.FILES)
        if goat_cen.is_valid():
            goat_cen.save()
            messages.success(request, 'Entry Saved')
            goat_cen = GoatCen()
    else:
        goat_cen = GoatCen()
    return render(request, 'goat-cen.html', {'goat_cen': goat_cen})

@login_required(login_url='/admin-page/login')
def cen_pig(request):
    if request.method == 'POST':
        pig_cen = PigCen(request.POST, request.FILES)
        if pig_cen.is_valid():
            pig_cen.save()
            messages.success(request, 'Entry Saved')
            pig_cen = PigCen()
    else:
        pig_cen = PigCen()
    return render(request, 'pig-cen.html', {'pig_cen': pig_cen})


@login_required(login_url='/admin-page/login')
def cen_sheep(request):
    if request.method == 'POST':
        sheep_cen = SheepCen(request.POST, request.FILES)
        if sheep_cen.is_valid():
            sheep_cen.save()
            messages.success(request, 'Entry Saved')
            sheep_cen = SheepCen()
    else:
        sheep_cen = SheepCen()
    return render(request, 'sheep-cen.html', {'sheep_cen': sheep_cen})

@login_required(login_url='/admin-page/login')
def cencow_view(request):
    cencowv = CowCensusPop.objects.order_by('-date')
    paginateccv = Paginator(cencowv, 12)
    page_number = request.GET.get('page')
    ccv_page_obj = paginateccv.get_page(page_number)
    context = {
        'ccv_page_obj' : ccv_page_obj,
    }
    return render(request, 'cow-cenv.html', context)

@login_required(login_url='/admin-page/login')
def cengoat_view(request):
    cengoatv = GoatCensusPop.objects.order_by('-date')
    paginategcv = Paginator(cengoatv, 12)
    page_number = request.GET.get('page')
    gcv_page_obj = paginategcv.get_page(page_number)
    context = {
        'gcv_page_obj' : gcv_page_obj,
    }
    return render(request, 'goat-cenv.html', context)

@login_required(login_url='/admin-page/login')
def cenpig_view(request):
    cenpigv = PigCensusPop.objects.order_by('-date')
    paginatepcv = Paginator(cenpigv, 12)
    page_number = request.GET.get('page')
    pcv_page_obj = paginatepcv.get_page(page_number)
    context = {
        'pcv_page_obj' : pcv_page_obj,
    }
    return render(request, 'pig-cenv.html',context)

@login_required(login_url='/admin-page/login')
def censheep_view(request):
    censheepv = SheepCensusPop.objects.order_by('-date')
    paginatescv = Paginator(censheepv, 12)
    page_number = request.GET.get('page')
    scv_page_obj = paginatescv.get_page(page_number)
    context = {
        'scv_page_obj' : scv_page_obj,
    }
    return render(request, 'sheep-cenv.html', context)

@login_required(login_url='/admin-page/login')
def cow_chart(request):
    cowmot_char = CowMortality.objects.all()
    month_cow = cowmot_char.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('bull_num') + F('cow_num') + F('calves')))
    cowpop_char = CowCensusPop.objects.order_by('-date')[:12]
    context ={
        'cmot' : month_cow,
        'cpop' : cowpop_char,
    }
    return render(request, 'cow-chart.html', context)

@login_required(login_url='/admin-page/login')
def goat_chart(request):
    goatmot_char = GoatMortality.objects.all()
    month_goat = goatmot_char.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('buck_num') + F('doe_num') + F('kid')))
    goatpop_char = GoatCensusPop.objects.order_by('-date')[:12]
    context ={
        'gmot' : month_goat,
        'gpop' : goatpop_char,
    }
    return render(request, 'goat-chart.html', context)

@login_required(login_url='/admin-page/login')
def sheep_chart(request):
    sheepmot_char = SheepMortality.objects.all()
    month_sheep = sheepmot_char.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('ram_num') + F('ewe_num') + F('lamb')))
    sheeppop_char = SheepCensusPop.objects.order_by('-date')[:12]
    context ={
        'smot' : month_sheep,
        'spop' : sheeppop_char,
    }
    return render(request, 'sheep-chart.html', context)

@login_required(login_url='/admin-page/login')
def pig_chart(request):
    pigmot_char = PigMortality.objects.all()
    month_pig = pigmot_char.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('boar_num') + F('sow_num') + F('pigglet')))
    pigpop_char = PigCensusPop.objects.order_by('-date')[:12]
    context ={
        'pmot' : month_pig,
        'ppop' : pigpop_char,
    }
    return render(request, 'pig-chart.html', context)

@login_required(login_url='/admin-page/login')
def delete_cowpop(request, cenc_id):
    post_record = get_object_or_404(CowCensusPop, id=cenc_id)
    post_record.delete()
    return redirect('farmrecord:cencow_view')

@login_required(login_url='/admin-page/login')
def delete_pigpop(request, cenp_id):
    post_record = get_object_or_404(PigCensusPop, id=cenp_id)
    post_record.delete()
    return redirect('farmrecord:cenpig_view')

@login_required(login_url='/admin-page/login')
def delete_goatpop(request, ceng_id):
    post_record = get_object_or_404(GoatCensusPop, id=ceng_id)
    post_record.delete()
    return redirect('farmrecord:cengoat_view')

@login_required(login_url='/admin-page/login')
def delete_sheeppop(request, cens_id):
    post_record = get_object_or_404(SheepCensusPop, id=cens_id)
    post_record.delete()
    return redirect('farmrecord:censheep_view')

@login_required(login_url='/admin-page/login')
def review_com(request):
    comment = Notification.objects.filter(user=request.user).order_by('-date')
    n = Notification.objects.filter(user=request.user, viewed=False)
    return render(request, 'message-list.html', {'comment': comment, 'notes' : n})

@login_required(login_url='/admin-page/login')
def comlist_view(request, slug):
    comment_view = Notification.objects.get(slug=slug)
    return render(request, 'message-view-note.html', {'Mesview': comment_view})






