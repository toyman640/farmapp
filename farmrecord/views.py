from django.shortcuts import get_object_or_404, redirect, render
from farmrecord.forms import *
from django.contrib import messages
from django.http import HttpResponse

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
    else:
        cow_mot = CowmotForm()
    return render(request, 'cow-motrep.html',{'cow_mot': cow_mot})

def cow_cull(request):
    if request.method == 'POST':
        cow_cull = CowcullForm(request.POST, request.FILES)
        if cow_cull.is_valid():
            cow_cull.save()
            messages.success(request, 'Entry Saved')
    else:
        cow_cull = CowcullForm()
    return render(request, 'cow-cull.html', {'cow_cull': cow_cull})

def cow_proc(request):
    if request.method == 'POST':
        cow_proc = CowprocForm(request.POST, request.FILES)
        if cow_proc.is_valid():
            cow_proc.save()
            messages.success(request, 'Entry Saved')
    else:
        cow_proc = CowprocForm()
    return render(request, 'cow-proc.html', {'cow_proc': cow_proc})


def cow_sales(request):
    if request.method == 'POST':
        cow_sale = CowsaleForm(request.POST, request.FILES)
        if cow_sale.is_valid():
            cow_sale.save()
            messages.success(request, 'Entry Saved')
    else:
        cow_sale = CowsaleForm()
    return render(request, 'cow-sale.html', {'cow_sale': cow_sale})

def cow_birth(request):
    return render(request, 'cow-birth.html')

def cow_motrec(request):
    cow_rec =   CowMortality.objects.order_by('date')
    return render(request, 'cowmotrec.html', {'cow_rec': cow_rec})

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
    cow_prec = CowProcurement.objects.order_by('date')
    return render(request, 'cowprocrec.html', {'cow_prec': cow_prec})

def cow_cullrec(request):
    cow_crec = CowCulling.objects.order_by('date')
    return render(request, 'cowcullrec.html', {'cow_crec': cow_crec})

def cow_salerec(request):
    cow_srec = CowSale.objects.order_by('date')
    return render(request, 'cowsalerec.html', {'cow_srec': cow_srec})

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
    else:
        goat_mot = GoatmotForm()
    return render(request, 'goat-motrep.html',{'goat_mot': goat_mot})


def goat_proc(request):
    if request.method == 'POST':
        goat_proc = GoatprocForm(request.POST, request.FILES)
        if goat_proc.is_valid():
            goat_proc.save()
            messages.success(request, 'Entry Saved')
    else:
        goat_proc = GoatprocForm()
    return render(request, 'goat-proc.html', {'goat_proc': goat_proc})

def goat_sales(request):
    if request.method == 'POST':
        goat_sale = GoatsaleForm(request.POST, request.FILES)
        if goat_sale.is_valid():
            goat_sale.save()
            messages.success(request, 'Entry Saved')
    else:
        goat_sale = GoatsaleForm()
    return render(request, 'goat-sale.html', {'goat_sale': goat_sale})

def goat_motrec(request):
    goat_mrec =   GoatMortality.objects.order_by('date')
    return render(request, 'goatmotrec.html', {'goat_mrec': goat_mrec})

def goat_procrec(request):
    goat_prec = GoatProcurement.objects.order_by('date')
    return render(request, 'goatprocrec.html', {'goat_prec' : goat_prec})

def goat_cullrec(request):
    goat_crec = GoatCulling.objects.order_by('date')
    return render(request, 'goatcullrec.html', {'goat_crec': goat_crec})

def goat_salerec(request):
    goat_srec = GoatSale.objects.order_by('date')
    return render(request, 'goatsalerec.html', {'goat_srec': goat_srec})

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
    else:
        pig_cull = PigcullForm()
    return render(request, 'pig-cull.html', {'pig_cull': pig_cull})

def pig_motrep(request):
    if request.method == 'POST':
        pig_mot = PigmotForm(request.POST, request.FILES)
        if pig_mot.is_valid():
            pig_mot.save()
            messages.success(request, 'Entry Saved')
    else:
        pig_mot = PigmotForm()
    return render(request, 'pig-motrep.html',{'pig_mot': pig_mot})


def pig_proc(request):
    if request.method == 'POST':
        pig_proc = PigprocForm(request.POST, request.FILES)
        if pig_proc.is_valid():
            pig_proc.save()
            messages.success(request, 'Entry Saved')
    else:
        pig_proc = PigprocForm()
    return render(request, 'pig-proc.html', {'pig_proc': pig_proc})

def pig_motrec(request):
    pig_mrec =   PigMortality.objects.order_by('date')
    return render(request, 'pigmotrec.html', {'pig_mrec': pig_mrec})

def pig_procrec(request):
    pig_prec = PigProcurement.objects.order_by('date')
    return render(request, 'pigprocrec.html', {'pig_rec': pig_prec})
    
def pig_salerec(request):
    pig_srec = PigSale.objects.order_by('date')
    return render(request, 'pigsalerec.html', {'pig_srec': pig_srec})

def pig_cullrec(request):
    pig_crec = PigCulling.objects.order_by('date')
    return render(request, 'pigcullrec.html', {'pig_crec': pig_crec})

def pig_procrec_view(request, abt_id):
    Pview = PigProcurement.objects.get(id=abt_id)
    return render(request, 'pigprocrec-view.html', {'Pview':Pview})

def pig_motrec_view(request, abt_id):
    Mview = PigMortality.objects.get(id=abt_id)
    return render(request, 'pigmotrec-view.html', {'Mview':Mview})

def pig_salerec_view(request, abt_id):
    Sview = PigSale.objects.get(id=abt_id)
    return render(request, 'pigsalerec-view.html', {'Sview':Sview})

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
    else:
        sheep_cull = SheepcullForm()
    return render(request, 'sheep-cull.html', {'sheep_cull': sheep_cull})


def sheep_motrep(request):
    if request.method == 'POST':
        sheep_mot = SheepmotForm(request.POST, request.FILES)
        if sheep_mot.is_valid():
            sheep_mot.save()
            messages.success(request, 'Entry Saved')
    else:
        sheep_mot = SheepmotForm()
    return render(request, 'sheep-mot.html',{'sheep_mot': sheep_mot})


def sheep_proc(request):
    if request.method == 'POST':
        sheep_proc = SheepprocForm(request.POST, request.FILES)
        if sheep_proc.is_valid():
            sheep_proc.save()
            messages.success(request, 'Entry Saved')
    else:
        sheep_proc = SheepprocForm()
    return render(request, 'sheep-proc.html', {'sheep_proc': sheep_proc})


def sheep_sales(request):
    if request.method == 'POST':
        sheep_sale = SheepsaleForm(request.POST, request.FILES)
        if sheep_sale.is_valid():
            sheep_sale.save()
            messages.success(request, 'Entry Saved')
    else:
        sheep_sale = SheepsaleForm()
    return render(request, 'sheep-sales.html', {'sheep_sale': sheep_sale})

def sheep_motrec(request):
    sheep_mrec = SheepMortality.objects.order_by('date')
    return render(request, 'sheepmotrec.html', {'sheep_mrec': sheep_mrec})

def sheep_procrec(request):
    sheep_prec = SheepProcurement.objects.order_by('date')
    return render(request, 'sheepprocrec.html', {'sheep_prec': sheep_prec})

def sheep_cullrec(request):
    sheep_crec = SheepCulling.objects.order_by('date')
    return render(request, 'sheepcullrec.html', {'sheep_crec': sheep_crec})

def sheep_salerec(request):
    sheep_srec = SheepSale.objects.order_by('date')
    return render(request, 'sheepsalerec.html', {'sheep_srec': sheep_srec})

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
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Egoatmot.html', {'edit_keycm': edit_motc})

def edit_sheepmot(request, post_id):
    single_log = get_object_or_404(SheepMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Esheepmot.html', {'edit_keycm': edit_motc})

def edit_pigmot(request, post_id):
    single_log = get_object_or_404(PigMortality, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Epigmot.html', {'edit_keycm': edit_motc})

def edit_cowsale(request, post_id):
    single_log = get_object_or_404(CowSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Ecowsale.html', {'edit_keycm': edit_motc})


def edit_goatsale(request, post_id):
    single_log = get_object_or_404(GoatSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Egoatsale.html', {'edit_keycm': edit_motc})

def edit_pigsale(request, post_id):
    single_log = get_object_or_404(PigSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Epigsale.html', {'edit_keycm': edit_motc})

def edit_sheepsale(request, post_id):
    single_log = get_object_or_404(SheepSale, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Esheepsale.html', {'edit_keycm': edit_motc})

def edit_cowproc(request, post_id):
    single_log = get_object_or_404(CowProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Ecowproc.html', {'edit_keycm': edit_motc})

def edit_goatproc(request, post_id):
    single_log = get_object_or_404(GoatProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Egoatproc.html', {'edit_keycm': edit_motc})

def edit_pigproc(request, post_id):
    single_log = get_object_or_404(PigProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Epigproc.html', {'edit_keycm': edit_motc})

def edit_sheepproc(request, post_id):
    single_log = get_object_or_404(SheepProcurement, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Esheepproc.html', {'edit_keycm': edit_motc})

def edit_cowcull(request, post_id):
    single_log = get_object_or_404(CowCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Ecowcull.html', {'edit_keycm': edit_motc})

def edit_goatcull(request, post_id):
    single_log = get_object_or_404(GoatCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Egoatcull.html', {'edit_keycm': edit_motc})

def edit_sheepcull(request, post_id):
    single_log = get_object_or_404(SheepCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Esheepcull.html', {'edit_keycm': edit_motc})

def edit_pigcull(request, post_id):
    single_log = get_object_or_404(PigCulling, id=post_id)
    if request.method == 'POST':
        edit_motc = EditcowMot(request.POST, request.FILES, instance=single_log)
        if edit_motc.is_valid():
            edit_motc.save()
            messages.success(request, 'Edited Successfully')
    else:
        edit_motc = EditcowMot(instance=single_log)
    return render(request, 'Epigcull.html', {'edit_keycm': edit_motc})