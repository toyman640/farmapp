from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .models import Drug, Dispatch, Unit
from .forms import DrugForm, DispatchForm, UnitForm
from django.core.paginator import Paginator

# Create your views here.
def drug_index(request):
  unit_form = UnitForm()
  dispatch_form = DispatchForm()
  units = Unit.objects.all()
  return render(request, 'drugapp/index.html', {'unit_form': unit_form, 'units': units, 'dispatch_form': dispatch_form})


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
            return redirect('drugapp:add_drug')
    else:
      form = DrugForm()
    
    return render(request, 'drugapp/add-drugs.html', {'form': form})


def drugs_list(request):
  drugs = Drug.objects.all()
  paginator = Paginator(drugs, 1)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'drugapp/drug-records.html', {'page_obj': page_obj})

# def dispatch_drug(request):
#     DispatchFormSet = formset_factory(DispatchForm, extra=3)

#     if request.method == 'POST':
#         formset = DispatchFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:
#                     dispatch = form.save(commit=False)
#                     dispatch.dispatched_by = request.user
#                     dispatch.save()
#             messages.success(request, "Drugs dispatched successfully!")
#             return redirect('dispatch_drug')
#     else:
#       formset = DispatchFormSet()
    
#     return render(request, 'inventory/dispatch_drug.html', {'formset': formset})

# def dispatch_drug(request):
#   DispatchFormSet = formset_factory(DispatchForm)  # No extra forms by default

#   if request.method == 'POST':
#     formset = DispatchFormSet(request.POST)
#     if formset.is_valid():
#         for form in formset:
#             if form.cleaned_data:
#                 dispatch = form.save(commit=False)
#                 dispatch.dispatched_by = request.user
#                 dispatch.save()
#         messages.success(request, "Drugs dispatched successfully!")
#         return redirect('dispatch_drug')
#   else:
#     formset = DispatchFormSet()  # Create an empty formset for GET requests
  
#   return render(request, 'drugapp/dispatch-drug.html', {'formset': formset})

def dispatch_drug(request):
    DispatchFormSet = formset_factory(DispatchForm, extra=0)  # No extra forms initially

    if request.method == 'POST':
        formset = DispatchFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    dispatch = form.save(commit=False)
                    dispatch.dispatched_by = request.user  # Assign the user
                    dispatch.save()  # Save dispatch record (stock reduction happens in `save()` method)
            messages.success(request, "Drugs dispatched successfully!")
            return redirect('drugapp:dispatch_drug')  
        else:
            messages.error(request, "There was an error in the form.")

    else:
        formset = DispatchFormSet()
    return render(request, 'drugapp/dispatch-drug.html', {'formset': formset})

