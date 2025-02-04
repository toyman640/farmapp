from django.http import JsonResponse
from django.shortcuts import render, redirect
from collections import defaultdict
from django.utils.timezone import localtime, now
from django.db.models import Sum
from datetime import timedelta
from django.db.models import F
from django.contrib import messages
from django.forms import formset_factory
from .models import Drug, Dispatch, Unit
from .forms import DrugForm, DispatchForm, UnitForm
from django.core.paginator import Paginator

# Create your views here.
# def drug_index(request):
#   unit_form = UnitForm()
#   dispatch_form = DispatchForm()
#   units = Unit.objects.all()
#   low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))
#   return render(request, 'drugapp/index.html', {'unit_form': unit_form, 'units': units, 'dispatch_form': dispatch_form})

def drug_index(request):
  unit_form = UnitForm()
  dispatch_form = DispatchForm()
  units = Unit.objects.all()
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))

  context = {
      'unit_form': unit_form,
      'dispatch_form': dispatch_form,
      'units': units,
      'low_stock_drugs': low_stock_drugs,  # Include the filtered drugs in the context
  }

  return render(request, 'drugapp/index.html', context)


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
    five_days_ago = now().date() - timedelta(days=5)
    dispatched = Dispatch.objects.filter(dispatched_at__date__gte=five_days_ago).order_by('-dispatched_at')
    DispatchFormSet = formset_factory(DispatchForm, extra=0)

    grouped_dispatches = defaultdict(list)
    for dispatch in dispatched:
      dispatch_date = localtime(dispatch.dispatched_at).date()
      grouped_dispatches[dispatch_date].append(dispatch)

    if request.method == 'POST':
      formset = DispatchFormSet(request.POST)
      if formset.is_valid():
        for form in formset:
          if form.cleaned_data:
            dispatch = form.save(commit=False)
            dispatch.dispatched_by = request.user
            dispatch.save()
        messages.success(request, "Drugs dispatched successfully!")
        return redirect('drugapp:dispatch_drug')  
      else:
          messages.error(request, "There was an error in the form.")

    else:
        formset = DispatchFormSet()
    return render(request, 'drugapp/dispatch-drug.html', {'formset': formset,  'grouped_dispatches': dict(grouped_dispatches) })

# def disptach_list(request):
#   dispatched = Dispatch.objects.all()
#   return render(request, 'drugapp/dispatch-drug.html', {'dispatched': dispatched})

def dismiss_low_stock(request):
  if request.method == "POST":
    drug_id = request.POST.get("drug_id")
    Drug.objects.filter(id=drug_id).update(restock_quantity_notify=0)  # Set notify level to 0 (hidden)
    return JsonResponse({"success": True})
  return JsonResponse({"success": False})

