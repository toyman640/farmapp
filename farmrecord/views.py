from django.shortcuts import get_object_or_404, redirect, render
from farmrecord.forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import format_html 
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models.aggregates import Count

# Create your views here.

def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

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

def cow_birth(request):
    return render(request, 'cow-birth.html')

def cow_motrec(request):
    cow_rec =   CowMortality.objects.order_by('-date')
    query_form = CowmotFilter()
    paginated_filtercm = Paginator(cow_rec, 10)
    page_number = request.GET.get('page')
    cm_page_obj = paginated_filtercm.get_page(page_number)
    cowmot_count = CowMortality.objects.all()
    aggregated = cowmot_count.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('mortality'))
    nums = "a" * cm_page_obj.paginator.num_pages
    context = {
        'cm_page_obj': cow_rec,
        'nums': nums,
        'q': query_form,
        'count' : aggregated
        
    }
    context['cm_page_obj'] = cm_page_obj
    return render(request, 'cowmotrec.html',context)

def cow_motrec_view(request, abt_id):
    mview = CowMortality.objects.get(id=abt_id)
    return render(request, 'cowmotrec-view.html', {'mview':mview})

def cow_procrec_view(request, abt_id):
    Pview = CowProcurement.objects.get(id=abt_id)
    return render(request, 'cowprocrec-view.html', {'Pview':Pview})

def cow_salerec_view(request, abt_id):
    Sview = CowSale.objects.get(id=abt_id)
    return render(request, 'cowsalerec-view.html', {'Sview':Sview})

def cow_cullrec_view(request, abtc_id):
    cview = CowCulling.objects.get(id=abtc_id)
    return render(request, 'cowcullrec-view.html', {'cview':cview})


def cow_procrec(request):
    cow_prec = CowProcurement.objects.order_by('-date')
    query_form = CowprocFilter()
    paginated_filtercp = Paginator(cow_prec, 10)
    page_number = request.GET.get('page')
    cp_page_obj = paginated_filtercp.get_page(page_number)
    nums = "a" * cp_page_obj.paginator.num_pages
    context = {
        'cm_page_obj': cow_prec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['cm_page_obj'] = cp_page_obj
    return render(request, 'cowprocrec.html', {'cow_prec': cow_prec}, context)

def cow_cullrec(request):
    cow_crec = CowCulling.objects.order_by('-date')
    query_form = CowcullFilter()
    paginated_filtercc = Paginator(cow_crec, 10)
    page_number = request.GET.get('page')
    cc_page_obj = paginated_filtercc.get_page(page_number)
    nums = "a" * cc_page_obj.paginator.num_pages
    context = {
        'cc_page_obj': cow_crec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['cc_page_obj'] = cc_page_obj
    return render(request, 'cowcullrec.html',context)

def cow_salerec(request):
    cow_srec = CowSale.objects.order_by('-date')
    query_form = CowsaleFilter()
    paginated_filtercs = Paginator(cow_srec, 10)
    page_number = request.GET.get('page')
    cs_page_obj = paginated_filtercs.get_page(page_number)
    nums = "a" * cs_page_obj.paginator.num_pages
    context = {
        'cs_page_obj': cow_srec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['cs_page_obj'] = cs_page_obj
    return render(request, 'cowsalerec.html',context)

def goat_birth(request):
    return render(request, 'goat-birth.html')

def goat_cull(request):
    if request.method == 'POST':
        goat_cull = GoatcullForm(request.POST, request.FILES)
        if goat_cull.is_valid():
            goat_cull.save()
            messages.success(request, 'Entry Saved')
    else:
        goat_cull = GoatcullForm()
    return render(request, 'goat-cull.html', {'goat_cull': goat_cull})

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

def goat_motrec(request):
    goat_mrec =   GoatMortality.objects.order_by('-date')
    query_form = GoatmotFilter()
    paginated_filtergm = Paginator(goat_mrec, 10)
    page_number = request.GET.get('page')
    gm_page_obj = paginated_filtergm.get_page(page_number)
    nums = "a" * gm_page_obj.paginator.num_pages
    context = {
        'gm_page_obj': goat_mrec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['gm_page_obj'] = gm_page_obj
    return render(request, 'goatmotrec.html', context)

def goat_procrec(request):
    goat_prec = GoatProcurement.objects.order_by('-date')
    query_form = GoatprocFilter()
    paginated_filtergp = Paginator(goat_prec, 10)
    page_number = request.GET.get('page')
    gp_page_obj = paginated_filtergp.get_page(page_number)
    nums = "a" * gp_page_obj.paginator.num_pages
    context = {
        'gp_page_obj': goat_prec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['gp_page_obj'] = gp_page_obj
    return render(request, 'goatprocrec.html',context)

def goat_cullrec(request):
    goat_crec = GoatCulling.objects.order_by('-date')
    query_form = GoatcullFilter()
    paginated_filtergc = Paginator(goat_crec, 10)
    page_number = request.GET.get('page')
    gc_page_obj = paginated_filtergc.get_page(page_number)
    nums = "a" * gc_page_obj.paginator.num_pages
    context = {
        'gc_page_obj': goat_crec,
        'nums': nums,
        'q'   : query_form
        
    }
    context['gc_page_obj'] = gc_page_obj
    return render(request, 'goatcullrec.html',context)

def goat_salerec(request):
    goat_srec = GoatSale.objects.order_by('-date')
    query_form = GoatsaleFilter()
    paginated_filtergs = Paginator(goat_srec, 10)
    page_number = request.GET.get('page')
    gs_page_obj = paginated_filtergs.get_page(page_number)
    nums = "a" * gs_page_obj.paginator.num_pages
    context = {
        'gs_page_obj': goat_srec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['gs_page_obj'] = gs_page_obj
    return render(request, 'goatsalerec.html',context)

def goat_motrec_view(request, abt_id):
    Mview = GoatMortality.objects.get(id=abt_id)
    return render(request, 'goatmotrec-view.html', {'Mview':Mview})

def goat_cullrec_view(request, abt_id):
    Cview = GoatCulling.objects.get(id=abt_id)
    return render(request, 'goatcullrecview.html', {'Cview':Cview})

def goat_salerec_view(request, abt_id):
    Sview = GoatSale.objects.get(id=abt_id)
    return render(request, 'goatsalerec-view.html', {'Sview':Sview})

def goat_procrec_view(request, abt_id):
    Pview = GoatProcurement.objects.get(id=abt_id)
    return render(request, 'goatprocrec-view.html', {'Pview':Pview})

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

def pig_birth(request):
    return render(request, 'pig-birth.html')

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

def pig_motrec(request):
    pig_mrec =   PigMortality.objects.order_by('-date')
    query_form = PigmotFilter()
    paginated_filterpm = Paginator(pig_mrec, 1)
    page_number = request.GET.get('page')
    pm_page_obj = paginated_filterpm.get_page(page_number)
    nums = "a" * pm_page_obj.paginator.num_pages
    context = {
        'pm_page_obj': pig_mrec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['pm_page_obj'] = pm_page_obj
    return render(request, 'pigmotrec.html', context)

def pig_procrec(request):
    pig_prec = PigProcurement.objects.order_by('-date')
    query_form = PigprocFilter()
    paginated_filterpp = Paginator(pig_prec, 10)
    page_number = request.GET.get('page')
    pp_page_obj = paginated_filterpp.get_page(page_number)
    nums = "a" * pp_page_obj.paginator.num_pages
    context = {
        'pp_page_obj': pig_prec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['pp_page_obj'] = pp_page_obj
    return render(request, 'pigprocrec.html', context)
    
def pig_salerec(request):
    pig_srec = PigSale.objects.order_by('-date')
    query_form = PigsaleFilter()
    paginated_filterps = Paginator(pig_srec, 10)
    page_number = request.GET.get('page')
    ps_page_obj = paginated_filterps.get_page(page_number)
    nums = "a" * ps_page_obj.paginator.num_pages
    context = {
        'ps_page_obj': pig_srec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['ps_page_obj'] = ps_page_obj
    return render(request, 'pigsalerec.html',context)

def pig_cullrec(request):
    pig_crec = PigCulling.objects.order_by('-date')
    query_form = PigcullFilter() 
    paginated_filterpc = Paginator(pig_crec, 10)
    page_number = request.GET.get('page')
    pc_page_obj = paginated_filterpc.get_page(page_number)
    nums = "a" * pc_page_obj.paginator.num_pages
    context = {
        'pc_page_obj': pig_crec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['pc_page_obj'] = pc_page_obj
    return render(request, 'pigcullrec.html', context)

def pig_procrec_view(request, abt_id):
    Pview = PigProcurement.objects.get(id=abt_id)
    return render(request, 'pigprocrec-view.html', {'Pview':Pview})

def pig_motrec_view(request, abt_id):
    Mview = PigMortality.objects.get(id=abt_id)
    return render(request, 'pigmotrec-view.html', {'Mview':Mview})

def pig_salerec_view(request, abt_id):
    Sview = PigSale.objects.get(id=abt_id)
    return render(request, 'pigsalerecview.html', {'Sview':Sview})

def pig_cullrec_view(request, abt_id):
    Cview = PigCulling.objects.get(id=abt_id)
    return render(request, 'pigcullrecview.html', {'Cview':Cview})


def sheep_birth(request):
    return render(request, 'sheep-birth.html')

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

def sheep_motrec(request):
    sheep_mrec = SheepMortality.objects.order_by('-date')
    query_form = SheepmotFilter() 
    paginated_filtersm = Paginator(sheep_mrec, 10)
    page_number = request.GET.get('page')
    sm_page_obj = paginated_filtersm.get_page(page_number)
    nums = "a" * sm_page_obj.paginator.num_pages
    context = {
        'sm_page_obj': sheep_mrec,
        'nums': nums,
        'q'   : query_form
        
    }
    context['sm_page_obj'] = sm_page_obj
    return render(request, 'sheepmotrec.html',context)

def sheep_procrec(request):
    sheep_prec = SheepProcurement.objects.order_by('-date')
    query_form = SheepprocFilter()
    paginated_filtersp = Paginator(sheep_prec, 10)
    page_number = request.GET.get('page')
    sp_page_obj = paginated_filtersp.get_page(page_number)
    nums = "a" * sp_page_obj.paginator.num_pages
    context = {
        'sp_page_obj': sheep_prec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['sp_page_obj'] = sp_page_obj
    return render(request, 'sheepprocrec.html',context)

def sheep_cullrec(request):
    sheep_crec = SheepCulling.objects.order_by('-date')
    query_form = SheepcullFilter()
    paginated_filtersc = Paginator(sheep_crec, 10)
    page_number = request.GET.get('page')
    sc_page_obj = paginated_filtersc.get_page(page_number)
    nums = "a" * sc_page_obj.paginator.num_pages
    context = {
        'sc_page_obj': sheep_crec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['sc_page_obj'] = sc_page_obj
    return render(request, 'sheepcullrec.html',context)

def sheep_salerec(request):
    sheep_srec = SheepSale.objects.order_by('-date')
    query_form = SheepsaleFilter() 
    paginated_filterss = Paginator(sheep_srec, 10)
    page_number = request.GET.get('page')
    ss_page_obj = paginated_filterss.get_page(page_number)
    nums = "a" * ss_page_obj.paginator.num_pages
    context = {
        'ss_page_obj': sheep_srec,
        'nums': nums,
        'q'    : query_form
        
    }
    context['ss_page_obj'] = ss_page_obj
    return render(request, 'sheepsalerec.html',context)

def sheep_motrec_view(request, abt_id):
    Mview = SheepMortality.objects.get(id=abt_id)
    return render(request, 'sheepmotrec-view.html', {'Mview':Mview})

def sheep_procrec_view(request, abt_id):
    Pview = SheepProcurement.objects.get(id=abt_id)
    return render(request, 'sheepprocrec-view.html', {'Pview':Pview})

def sheep_salerec_view(request, abt_id):
    Sview = SheepSale.objects.get(id=abt_id)
    return render(request, 'sheepsalerec-view.html', {'Sview':Sview})

def sheep_cullrec_view(request, abt_id):
    Cview = SheepCulling.objects.get(id=abt_id)
    return render(request, 'sheepcullrec-view.html', {'Cview':Cview})


def delete_postc(request, listf_id):
    post_record = get_object_or_404(CowMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:cow_motrec')

def delete_postg(request, listg_id):
    post_record = get_object_or_404(GoatMortality, id=listg_id)
    post_record.delete()
    return redirect('farmrecord:goat_motrec')

def delete_posts(request, listf_id):
    post_record = get_object_or_404(SheepMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:sheep_motrec')

def delete_postp(request, listf_id):
    post_record = get_object_or_404(PigMortality, id=listf_id)
    post_record.delete()
    return redirect('farmrecord:pig_motrec')

def delete_postcullg(request, listcullg_id):
    post_record = get_object_or_404(GoatCulling, id=listcullg_id)
    post_record.delete()
    return redirect('farmrecord:goat_cullrec')

def delete_postcullp(request, listcullp_id):
    post_record = get_object_or_404(PigCulling, id=listcullp_id)
    post_record.delete()
    return redirect('farmrecord:pig_cullrec')

def delete_postculls(request, listculls_id):
    post_record = get_object_or_404(SheepCulling, id=listculls_id)
    post_record.delete()
    return redirect('farmrecord:sheep_cullrec')

def delete_postcullc(request, listcullc_id):
    post_record = get_object_or_404(CowCulling, id=listcullc_id)
    post_record.delete()
    return redirect('farmrecord:cow_cullrec')

def delete_postsalec(request, listsalec_id):
    post_record = get_object_or_404(CowSale, id=listsalec_id)
    post_record.delete()
    return redirect('farmrecord:cow_salerec')

def delete_postsaleg(request, listsaleg_id):
    post_record = get_object_or_404(GoatSale, id=listsaleg_id)
    post_record.delete()
    return redirect('farmrecord:goat_salerec')

def delete_postsalep(request, listsalep_id):
    post_record = get_object_or_404(PigSale, id=listsalep_id)
    post_record.delete()
    return redirect('farmrecord:pig_salerec')

def delete_postsales(request, listsales_id):
    post_record = get_object_or_404(SheepSale, id=listsales_id)
    post_record.delete()
    return redirect('farmrecord:sheep_salerec')

def delete_postprocc(request, listprocc_id):
    post_record = get_object_or_404(CowProcurement, id=listprocc_id)
    post_record.delete()
    return redirect('farmrecord:cow_procrec')

def delete_postprocg(request, listprocg_id):
    post_record = get_object_or_404(GoatProcurement, id=listprocg_id)
    post_record.delete()
    return redirect('farmrecord:goat_procrec')

def delete_postprocp(request, listprocp_id):
    post_record = get_object_or_404(PigProcurement, id=listprocp_id)
    post_record.delete()
    return redirect('farmrecord:pig_procrec')

def delete_postprocs(request, listprocs_id):
    post_record = get_object_or_404(SheepProcurement, id=listprocs_id)
    post_record.delete()
    return redirect('farmrecord:sheep_procrec')

def edit_cowmot(request, post_id):
    single_log = get_object_or_404(CowMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Ecowmot.html', {'edit_keycm': edit_motc})

def edit_goatmot(request, post_id):
    single_log = get_object_or_404(GoatMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditgoatMot(instance=single_log)
    return render(request, 'Egoatmot.html', {'edit_keycm': edit_motc})

def edit_sheepmot(request, post_id):
    single_log = get_object_or_404(SheepMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditsheepMot(instance=single_log)
    return render(request, 'Esheepmot.html', {'edit_keycm': edit_motc})

def edit_pigmot(request, post_id):
    single_log = get_object_or_404(PigMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditpigMot(instance=single_log)
    return render(request, 'Epigmot.html', {'edit_keycm': edit_motc})

def edit_cowsale(request, post_id):
    single_log = get_object_or_404(CowSale, id=post_id)
    if request.method == 'POST':
        edit_salec = EditcowSale(request.POST, request.FILES, instance=single_log)
        if edit_salec.is_valid():
            edit_salec.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_salec = EditcowSale(instance=single_log)
    return render(request, 'Ecowsale.html', {'edit_keycs': edit_salec})


def edit_goatsale(request, post_id):
    single_log = get_object_or_404(GoatSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditgoatSale(instance=single_log)
    return render(request, 'Egoatsale.html', {'edit_keycm': edit_motc})

def edit_pigsale(request, post_id):
    single_log = get_object_or_404(PigSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditpigSale(instance=single_log)
    return render(request, 'Epigsale.html', {'edit_keycm': edit_motc})

def edit_sheepsale(request, post_id):
    single_log = get_object_or_404(SheepSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepSale(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditsheepSale(instance=single_log)
    return render(request, 'Esheepsale.html', {'edit_keycm': edit_motc})

def edit_cowproc(request, post_id):
    single_log = get_object_or_404(CowProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowProc(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowProc(instance=single_log)
    return render(request, 'Ecowproc.html', {'edit_keycm': edit_motc})

def edit_goatproc(request, post_id):
    single_log = get_object_or_404(GoatProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatProc(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditgoatProc(instance=single_log)
    return render(request, 'Egoatproc.html', {'edit_keycm': edit_motc})

def edit_pigproc(request, post_id):
    single_log = get_object_or_404(PigProcurement, id=post_id)
    if request.method == 'POST':
        edit_procp = EditpigProc(request.POST, request.FILES, instance=single_log)
        if edit_procp.is_valid():
            edit_procp.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_procp = EditpigProc(instance=single_log)
    return render(request, 'Epigproc.html', {'edit_procp': edit_procp})

def edit_sheepproc(request, post_id):
    single_log = get_object_or_404(SheepProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepProc(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Esheepproc.html', {'edit_keycm': edit_motc})

def edit_cowcull(request, post_id):
    single_log = get_object_or_404(CowCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowCull(instance=single_log)
    return render(request, 'Ecowcull.html', {'edit_keycm': edit_motc})

def edit_goatcull(request, post_id):
    single_log = get_object_or_404(GoatCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditgoatCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditgoatCull(instance=single_log)
    return render(request, 'Egoatcull.html', {'edit_keycm': edit_motc})

def edit_sheepcull(request, post_id):
    single_log = get_object_or_404(SheepCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditsheepCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, format_html('Edited Successfully, click here to go back <a href="/pages/sheep-cull-records">link</a>'))
    else:
        edit_motc = EditsheepCull(instance=single_log)
    return render(request, 'Esheepcull.html', {'edit_keycm': edit_motc})

def edit_pigcull(request, post_id):
    single_log = get_object_or_404(PigCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditpigCull(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditpigCull(instance=single_log)
    return render(request, 'Epigcull.html', {'edit_keycm': edit_motc})

def cowmot_filter(request):
    if request.method == 'GET':
        cowmot_query = CowmotFilter(request.GET)
        if cowmot_query.is_valid():
            start_date = cowmot_query.cleaned_data.get('start_date')
            end_date = cowmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowMortality.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-cowmot.html', {'queryset': result, 'q': cowmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowmot_query = CowmotFilter()
    return render(request, 'filter-cowmot.html', {'q': cowmot_query})

def goatmot_filter(request):
    if request.method == 'GET':
        goatmot_query = GoatmotFilter(request.GET)
        if goatmot_query.is_valid():
            start_date = goatmot_query.cleaned_data.get('start_date')
            end_date = goatmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatMortality.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-goatmot.html', {'queryset': result, 'q': goatmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatmot_query = GoatmotFilter()
    return render(request, 'filter-goatmot.html', {'q': goatmot_query})

def pigmot_filter(request):
    if request.method == 'GET':
        pigmot_query = PigmotFilter(request.GET)
        if pigmot_query.is_valid():
            start_date = pigmot_query.cleaned_data.get('start_date')
            end_date = pigmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigMortality.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-pigmot.html', {'queryset': result, 'q': pigmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigmot_query = PigmotFilter()
    return render(request, 'filter-pigmot.html', {'q': pigmot_query})

def sheepmot_filter(request):
    if request.method == 'GET':
        sheepmot_query = SheepmotFilter(request.GET)
        if sheepmot_query.is_valid():
            start_date = sheepmot_query.cleaned_data.get('start_date')
            end_date = sheepmot_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepMortality.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepmot.html', {'queryset': result, 'q': sheepmot_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepmot_query = SheepmotFilter()
    return render(request, 'filter-sheepmot.html', {'q': sheepmot_query})

def sheepsale_filter(request):
    if request.method == 'GET':
        sheepsale_query = SheepsaleFilter(request.GET)
        if sheepsale_query.is_valid():
            start_date = sheepsale_query.cleaned_data.get('start_date')
            end_date = sheepsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepSale.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepsale.html', {'queryset': result, 'q': sheepsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepsale_query = SheepsaleFilter()
    return render(request, 'filter-sheepsale.html', {'q': sheepsale_query})

def pigsale_filter(request):
    if request.method == 'GET':
        pigsale_query = PigsaleFilter(request.GET)
        if pigsale_query.is_valid():
            start_date = pigsale_query.cleaned_data.get('start_date')
            end_date = pigsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigSale.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-pigsale.html', {'queryset': result, 'q': pigsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigsale_query = PigsaleFilter()
    return render(request, 'filter-pigsale.html', {'q': pigsale_query})

def cowsale_filter(request):
    if request.method == 'GET':
        cowsale_query = CowsaleFilter(request.GET)
        if cowsale_query.is_valid():
            start_date = cowsale_query.cleaned_data.get('start_date')
            end_date = cowsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowSale.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-cowsale.html', {'queryset': result, 'q': cowsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowsale_query = CowsaleFilter()
    return render(request, 'filter-cowsale.html', {'q': cowsale_query})

def goatsale_filter(request):
    if request.method == 'GET':
        goatsale_query = GoatsaleFilter(request.GET)
        if goatsale_query.is_valid():
            start_date = goatsale_query.cleaned_data.get('start_date')
            end_date = goatsale_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatSale.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepsale.html', {'queryset': result, 'q': goatsale_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatsale_query = GoatsaleFilter()
    return render(request, 'filter-sheepsale.html', {'q': goatsale_query})

def sheepproc_filter(request):
    if request.method == 'GET':
        sheepproc_query = SheepprocFilter(request.GET)
        if sheepproc_query.is_valid():
            start_date = sheepproc_query.cleaned_data.get('start_date')
            end_date = sheepproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepProcurement.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepproc.html', {'queryset': result, 'q': sheepproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepproc_query = SheepprocFilter()
    return render(request, 'filter-sheepproc.html', {'q': sheepproc_query})

def pigproc_filter(request):
    if request.method == 'GET':
        pigproc_query = PigprocFilter(request.GET)
        if pigproc_query.is_valid():
            start_date = pigproc_query.cleaned_data.get('start_date')
            end_date = pigproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigProcurement.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-pigproc.html', {'queryset': result, 'q': pigproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigproc_query = PigprocFilter()
    return render(request, 'filter-pigproc.html', {'q': pigproc_query})

def cowproc_filter(request):
    if request.method == 'GET':
        cowproc_query = CowprocFilter(request.GET)
        if cowproc_query.is_valid():
            start_date = cowproc_query.cleaned_data.get('start_date')
            end_date = cowproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowProcurement.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepproc.html', {'queryset': result, 'q': cowproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowproc_query = CowprocFilter()
    return render(request, 'filter-sheepproc.html', {'q': cowproc_query})

def goatproc_filter(request):
    if request.method == 'GET':
        goatproc_query = GoatprocFilter(request.GET)
        if goatproc_query.is_valid():
            start_date = goatproc_query.cleaned_data.get('start_date')
            end_date = goatproc_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatProcurement.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-goatproc.html', {'queryset': result, 'q': goatproc_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatproc_query = GoatprocFilter()
    return render(request, 'filter-goatproc.html', {'q': goatproc_query})

def cowcull_filter(request):
    if request.method == 'GET':
        cowcull_query = CowcullFilter(request.GET)
        if cowcull_query.is_valid():
            start_date = cowcull_query.cleaned_data.get('start_date')
            end_date = cowcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = CowCulling.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-cowcull.html', {'queryset': result, 'b': cowcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        cowcull_query = CowcullFilter()
    return render(request, 'filter-cowcull.html', {'b': cowcull_query})


def goatcull_filter(request):
    if request.method == 'GET':
        goatcull_query = GoatcullFilter(request.GET)
        if goatcull_query.is_valid():
            start_date = goatcull_query.cleaned_data.get('start_date')
            end_date = goatcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = GoatCulling.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-goatcull.html', {'queryset': result, 'q': goatcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        goatcull_query = GoatcullFilter()
    return render(request, 'filter-goatcull.html', {'q': goatcull_query})

def sheepcull_filter(request):
    if request.method == 'GET':
        sheepcull_query = SheepcullFilter(request.GET)
        if sheepcull_query.is_valid():
            start_date = sheepcull_query.cleaned_data.get('start_date')
            end_date = sheepcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = SheepCulling.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-sheepcull.html', {'queryset': result, 'q': sheepcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        sheepcull_query = SheepcullFilter()
    return render(request, 'filter-sheepcull.html', {'q': sheepcull_query})

def pigcull_filter(request):
    if request.method == 'GET':
        pigcull_query = PigcullFilter(request.GET)
        if pigcull_query.is_valid():
            start_date = pigcull_query.cleaned_data.get('start_date')
            end_date = pigcull_query.cleaned_data.get('end_date')
            new_end = end_date + timedelta(days=1)
            result = PigCulling.objects.filter(date__range=[start_date, new_end])
            return render(request, 'filter-pigcull.html', {'queryset': result, 'q': pigcull_query})
        else:
            messages.error(request, 'Out of range')
    else:
        pigcull_query = PigcullFilter()
    return render(request, 'filter-pigcull.html', {'q': pigcull_query})


