from django.shortcuts import render
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
    return render(request, 'cow-cull.html', {'cow_proc': cow_proc})


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
    view = CowMortality.objects.get(id=abt_id)
    return render(request, 'cowmotrec-view.html', {'view':view})

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
        goat_cull = CowcullForm()
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
        goat_proc = CowprocForm(request.POST, request.FILES)
        if goat_proc.is_valid():
            goat_proc.save()
            messages.success(request, 'Entry Saved')
    else:
        goat_proc = GoatprocForm()
    return render(request, 'goat-cull.html', {'goat_proc': goat_proc})

def goat_sales(request):
    if request.method == 'POST':
        goat_sale = GoatsaleForm(request.POST, request.FILES)
        if goat_sale.is_valid():
            goat_sale.save()
            messages.success(request, 'Entry Saved')
    else:
        goat_sale = GoatsaleForm()
    return render(request, 'goat-cull.html', {'goat_sale': goat_sale})

def goat_motrec(request):
    goat_rec =   GoatMortality.objects.order_by('date')
    return render(request, 'goatmotrec.html', {'goat_rec': goat_rec})

def goat_procrec(request):
    goat_prec = GoatProcurement.objects.order_by('date')
    return render(request, 'goatprocrec.html', {'goat_prec' : goat_prec})

def goat_cullrec(request):
    goat_crec = GoatCulling.objects.order_by('date')
    return render(request, 'goatcullrec.html', {'goat_crec': goat_crec})

def goat_salerec(request):
    goat_srec = GoatSale.objects.order_by('date')
    return render(request, 'goatsalerec.html', {'goat_srec': goat_srec})

def pig_sales(request):
    if request.method == 'POST':
        pig_sale = PigsaleForm(request.POST, request.FILES)
        if pig_sale.is_valid():
            pig_sale.save()
            messages.success(request, 'Entry Saved')
    else:
        pig_sale = PigsaleForm()
    return render(request, 'pig-sale.html', {'pig_sale': pig_sale})

def pig_birth(request):
    return render(request, 'pig-birth.html')

def pig_cull(request):
    if request.method == 'POST':
        pig_cull = PigcullForm(request.POST, request.FILES)
        if pig_cull.is_valid():
            pig_cull.save()
            messages.success(request, 'Entry Saved')
    else:
        pig_cull = CowcullForm()
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
    pig_rec =   PigMortality.objects.order_by('date')
    return render(request, 'pigmotrec.html', {'pig_rec': pig_rec})

def pig_procrec(request):
    pig_prec = PigProcurement.objects.order_by('date')
    return render(request, 'pigprocrec.html', {'pig_rec': pig_prec})
    
def pig_salerec(request):
    pig_srec = PigSale.objects.order_by('date')
    return render(request, 'pigsalerec.html', {'pig_srec': pig_srec})

def pig_cullrec(request):
    pig_crec = PigCulling.objects.order_by('date')
    return render(request, 'pigcullrec.html', {'pig_crec': pig_crec})

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
    return render(request, 'cow-motrep.html',{'sheep_mot': sheep_mot})


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
    sheep_rec =   SheepMortality.objects.order_by('date')
    return render(request, 'sheepmotrec.html', {'sheep_rec': sheep_rec})

def sheep_procrec(request):
    sheep_prec = SheepProcurement.objects.order_by('date')
    return render(request, 'sheepprocrec.html', {'sheep_prec': sheep_prec})

def sheep_cullrec(request):
    sheep_crec = SheepCulling.objects.order_by('date')
    return render(request, 'sheepcullrec.html', {'sheep_crec': sheep_crec})

def sheep_salerec(request):
    sheep_srec = SheepSale.objects.order_by('date')
    return render(request, 'sheepsalerec.html', {'sheep_srec': sheep_srec})

