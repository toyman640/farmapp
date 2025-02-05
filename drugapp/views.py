from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from django.utils.timezone import localtime, now
from django.db.models import Sum
from datetime import timedelta
from django.db.models import F
from django.contrib import messages
from django.forms import formset_factory
from .models import Drug, Dispatch, Unit
from .forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


def drug_index(request):
  unit_form = UnitForm()
  dispatch_form = DispatchForm()
  units = Unit.objects.all()
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))

  context = {
      'unit_form': unit_form,
      'dispatch_form': dispatch_form,
      'units': units,
      'low_stock_drugs': low_stock_drugs,
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

# def add_drug(request):
#     if request.method == 'POST':
#         form = DrugForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Drug added successfully!")
#             return redirect('drugapp:add_drug')
#     else:
#       form = DrugForm()
    
#     return render(request, 'drugapp/add-drugs.html', {'form': form})

def add_drug(request):
  if request.method == 'POST':
    form = DrugForm(request.POST)
    if form.is_valid():
      form.save()
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX
        return JsonResponse({"success": True, "message": "Drug added successfully!"})
      messages.success(request, "Drug added successfully!")
      return redirect('drugapp:add_drug')
    else:
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
        return JsonResponse({"success": False, "message": "Error adding drug. Please check your input."})
  
  else:
    form = DrugForm()

  return render(request, 'drugapp/add-drugs.html', {'form': form})


def drugs_list(request):
  drugs = Drug.objects.all()
  paginator = Paginator(drugs, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'drugapp/drug-records.html', {'page_obj': page_obj})

def drug_detail(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  return render(request, 'drugapp/drug-info.html', {'drug': drug})

def dispatch_drug(request):
    five_days_ago = now().date() - timedelta(days=5)
    dispatched = Dispatch.objects.filter(dispatched_at__date__gte=five_days_ago).order_by('-dispatched_at')
    all_dispatch = Dispatch.objects.all().order_by('-dispatched_at')
    paginator = Paginator(all_dispatch, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    return render(request, 'drugapp/dispatch-drug.html', {'formset': formset, 'page_obj': page_obj, 'grouped_dispatches': dict(grouped_dispatches) })

def dismiss_low_stock(request):
  if request.method == "POST":
    drug_id = request.POST.get("drug_id")
    Drug.objects.filter(id=drug_id).update(restock_quantity_notify=0)
    return JsonResponse({"success": True})
  return JsonResponse({"success": False})



def edit_dispatch(request, dispatch_id):
  dispatch = get_object_or_404(Dispatch, id=dispatch_id)
  
  if request.method == "POST":
    form = DispatchEditForm(request.POST, instance=dispatch)
    if form.is_valid():
      # Save the form, which will trigger the save method on the Dispatch model
      try:
        form.save()  # The model logic handles stock updates
        return redirect('drugapp:dispatch_drug')  # Redirect to dispatch list page or wherever
      except ValueError as e:
        messages.error(request, str(e))  # Display error message if not enough stock
  else:
    form = DispatchEditForm(instance=dispatch)

  return render(request, 'drugapp/edit-dispatch.html', {'form': form, 'dispatch': dispatch})

def delete_dispatch(request, dispatch_id):
  dispatch = get_object_or_404(Dispatch, id=dispatch_id)

  if request.method == "POST":
    dispatch.delete()  # This will also restore the quantity in the `Drug` model
    messages.success(request, "Dispatch record deleted successfully!")
    return JsonResponse({"success": True, "message": "Dispatch record deleted successfully!"})

  return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def edit_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  if request.method == 'POST':
    form = DrugForm(request.POST, instance=drug)
    if form.is_valid():
      form.save()
      return redirect('drugapp:drugs_list')
  else:
    form = DrugForm(instance=drug)
  return render(request, 'drugapp/edit-drug.html', {'form': form, 'drug': drug})


def delete_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)

  if request.method == 'POST':
    drug.delete()
    return redirect('drugapp:drugs_list')

  return render(request, 'drugapp/confirm_delete.html', {'drug': drug})
