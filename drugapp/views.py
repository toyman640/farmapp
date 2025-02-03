from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Drug, Dispatch, Unit
from .forms import DrugForm, DispatchForm, UnitForm
from django.forms import formset_factory

# Create your views here.
def drug_index(request):
  unit_form = UnitForm()
  units = Unit.objects.all()
  return render(request, 'drugapp/index.html', {'unit_form': unit_form, 'units': units})

# def add_unit(request):
#     """ View to create a new Unit """
#     if request.method == 'POST':
#         form = UnitForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Unit added successfully!")
#             return redirect('add_unit')
#     else:
#         form = UnitForm()
    
#     return render(request, 'inventory/add_unit.html', {'form': form})


# def add_unit(request):
#   """ View to create a new Unit via modal """
#   if request.method == 'POST':
#     form = UnitForm(request.POST)
#     if form.is_valid():
#       form.save()
#       if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
#         return JsonResponse({'success': True})
#       messages.success(request, "Unit added successfully!")
#       return redirect('home')
#     else:
#       if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
#         return JsonResponse({'success': False, 'errors': form.errors})

#   else:
#     form = UnitForm()
  
#   return render(request, 'drupapp/index.html', {'form': form})


def add_unit(request):
  if request.method == 'POST':
    form = UnitForm(request.POST)
    if form.is_valid():
      form.save()
      return JsonResponse({"success": True})
    else:
      return JsonResponse({"success": False, "errors": form.errors})
  return JsonResponse({"success": False, "message": "Invalid request"})


def list_units(request):
  units = Unit.objects.all()
  return render(request, 'inventory/list_units.html', {'units': units})


def view_unit(request, unit_id):
  unit = get_object_or_404(Unit, id=unit_id)
  return render(request, 'drugapp/drug-records.html', {'unit': unit})

def add_drug(request):
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
    DispatchFormSet = formset_factory(DispatchForm, extra=3)

    if request.method == 'POST':
        formset = DispatchFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    dispatch = form.save(commit=False)
                    dispatch.dispatched_by = request.user
                    dispatch.save()
            messages.success(request, "Drugs dispatched successfully!")
            return redirect('dispatch_drug')
    else:
      formset = DispatchFormSet()
    
    return render(request, 'inventory/dispatch_drug.html', {'formset': formset})
