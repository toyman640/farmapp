from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

def cow_motrep(request):
    return render(request, 'cow-motrep.html')

def cow_cull(request):
    return render(request, 'cow-cull.html')

def cow_proc(request):
    return render(request, 'cow-proc.html')

def cow_sales(request):
    return render(request, 'cow-sale.html')

def cow_birth(request):
    return render(request, 'cow-birth.html')

def cow_rec(request):
    return render(request, 'cowmotrec.html')

def goat_birth(request):
    return render(request, 'goat-birth.html')

def goat_cull(request):
    return render(request, 'goat_cull.html')

def goat_motrep(request):
    return render(request, 'goat-motrep.html')

def goat_proc(request):
    return render(request, 'goat-proc.html')

def goat_sales(request):
    return render(request, 'goat-sale.html')

def goat_rec(request):
    return render(request, 'cowmotrec.html')

def pig_sales(request):
    return render(request, 'pig-sales.html')

def pig_birth(request):
    return render(request, 'pig-birth.html')

def pig_cull(request):
    return render(request, 'pig-cull.html')

def pig_motrep(request):
    return render(request, 'pig-motrep.html')

def pig_proc(request):
    return render(request, 'pig-proc.html')

def pig_rec(request):
    return render(request, 'cowmotrec.html')

def sheep_birth(request):
    return render(request, 'sheep-birth.html')

def sheep_cull(request):
    return render(request, 'sheep-cul.html')

def sheep_motrep(request):
    return render(request, 'sheep-mot.html')

def sheep_proc(request):
    return render(request, 'sheep-proc.html')

def sheep_sales(request):
    return render(request, 'sheep-sales.html')

def sheep_rec(request):
    return render(request, 'cowmotrec.html')

