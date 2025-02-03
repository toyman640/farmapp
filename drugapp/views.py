from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Drug, Dispatch, Unit
from .forms import DrugForm, DispatchForm, UnitForm
from django.forms import formset_factory

# Create your views here.
def drug_index(request):
  return render(request, 'drugapp/index.html')

def add_unit(request):
    """ View to create a new Unit """
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Unit added successfully!")
            return redirect('add_unit')
    else:
        form = UnitForm()
    
    return render(request, 'inventory/add_unit.html', {'form': form})

def add_drug(request):
    """ View to create a new Drug """
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Drug added successfully!")
            return redirect('add_drug')
    else:
        form = DrugForm()
    
    return render(request, 'inventory/add_drug.html', {'form': form})

def dispatch_drug(request):
    """ View to dispatch multiple drugs at once """
    DispatchFormSet = formset_factory(DispatchForm, extra=3)

    if request.method == 'POST':
        formset = DispatchFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:  # Avoid empty forms
                    dispatch = form.save(commit=False)
                    dispatch.dispatched_by = request.user
                    dispatch.save()
            messages.success(request, "Drugs dispatched successfully!")
            return redirect('dispatch_drug')
    else:
        formset = DispatchFormSet()
    
    return render(request, 'inventory/dispatch_drug.html', {'formset': formset})
