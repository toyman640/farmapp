from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from django.utils.timezone import localtime, now, localdate
from django.db.models import Sum
from datetime import timedelta
from django.db.models import F
from django.contrib import messages
from django.forms import formset_factory
from .models import Drug, Dispatch, Unit, InventoryLog
from .forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt


def drug_index(request):
  unit_form = UnitForm()
  units = Unit.objects.all()
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))
  today = localdate()
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)

  context = {
    'unit_form': unit_form,
    'units': units,
    'low_stock_drugs': low_stock_drugs,
    'today_dispatches': today_dispatches, 
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
#   if request.method == 'POST':
#     form = DrugForm(request.POST)
#     if form.is_valid():
#       form.save()
#       if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX
#         return JsonResponse({"success": True, "message": "Drug added successfully!"})
#       messages.success(request, "Drug added successfully!")
#       return redirect('drugapp:add_drug')
#     else:
#       if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
#         return JsonResponse({"success": False, "message": "Error adding drug. Please check your input."})
  
#   else:
#     form = DrugForm()

#   return render(request, 'drugapp/add-drugs.html', {'form': form})

def add_drug(request):
  if request.method == 'POST':
      form = DrugForm(request.POST)
      if form.is_valid():
          drug = form.save(commit=False)  # Don't save yet
          existing_drug = Drug.objects.filter(batch_number=drug.batch_number).first()
          
          if existing_drug:
              # If drug exists, update stock
              previous_quantity = existing_drug.quantity
              existing_drug.update_stock(previous_quantity + drug.quantity, request.user)
              messages.success(request, "Stock updated successfully!")
              return redirect('drugapp:drugs_list')
          else:
              # If new drug, save normally
              drug.save()
              InventoryLog.objects.create(
                  drug=drug,
                  previous_quantity=0,
                  new_quantity=drug.quantity,
                  updated_by=request.user
              )
              messages.success(request, "Drug added successfully!")

          if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX response
              return JsonResponse({"success": True, "message": "Drug added successfully!"})

          return redirect('drugapp:add_drug')

      else:
          if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
              return JsonResponse({"success": False, "message": "Error adding drug. Please check your input."})

  else:
      form = DrugForm()

  return render(request, 'drugapp/add-drugs.html', {'form': form})


def update_drug_quantity(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == "POST":
        form = UpdateDrugQuantityForm(request.POST)
        if form.is_valid():
            added_quantity = form.cleaned_data["quantity"]
            new_quantity = drug.quantity + added_quantity  # Add stock

            drug.update_stock(new_quantity, request.user)  # Use model method

            messages.success(request, "Stock updated successfully!")
            return redirect("drugapp:drugs_list")
    else:
        form = UpdateDrugQuantityForm()

    return render(request, "drugapp/update-drug.html", {"form": form, "drug": drug})

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
  dispatch_filter = DispatchFilter()
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
  return render(request, 'drugapp/dispatch-drug.html', {'formset': formset, 'dispatch_filter': dispatch_filter, 'page_obj': page_obj,'grouped_dispatches': dict(grouped_dispatches) })

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


def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
          correct_quantity = form.cleaned_data['quantity']

          drug.correct_stock(correct_quantity, request.user)

          messages.success(request, "Drug stock corrected successfully!")
          return redirect('drugapp:drugs_list')
    else:
        form = DrugForm(instance=drug)

    return render(request, 'drugapp/edit-drug.html', {'form': form, 'drug': drug})


def delete_dispatch(request, dispatch_id):
  dispatch = get_object_or_404(Dispatch, id=dispatch_id)

  if request.method == "POST":
    dispatch.delete()  # This will also restore the quantity in the `Drug` model
    messages.success(request, "Dispatch record deleted successfully!")
    return JsonResponse({"success": True, "message": "Dispatch record deleted successfully!"})

  return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

# def edit_drug(request, drug_id):
#   drug = get_object_or_404(Drug, id=drug_id)
#   if request.method == 'POST':
#     form = DrugForm(request.POST, instance=drug)
#     if form.is_valid():
#       form.save()
#       return redirect('drugapp:drugs_list')
#   else:
#     form = DrugForm(instance=drug)
#   return render(request, 'drugapp/edit-drug.html', {'form': form, 'drug': drug})


def delete_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)

  if request.method == 'POST':
    drug.delete()
    return redirect('drugapp:drugs_list')

  return render(request, 'drugapp/confirm_delete.html', {'drug': drug})


def dispatch_filter(request):
  if request.method == 'GET':
      dispatch_query = DispatchFilter(request.GET)
      if dispatch_query.is_valid():
          start_date = dispatch_query.cleaned_data.get('start_date')
          end_date = dispatch_query.cleaned_data.get('end_date')
          drug_name = dispatch_query.cleaned_data.get('drug_name')
          filters = {}

          # Apply filters
          if start_date:
              filters['dispatched_at__gte'] = start_date
          if end_date:
              filters['dispatched_at__lte'] = end_date
          if drug_name:
              filters['drug__drug_name__icontains'] = drug_name

          # Query the filtered dispatches
          result = Dispatch.objects.filter(**filters).order_by('-dispatched_at')
          print(result)

          return render(request, 'drugapp/filter-dispatch-list.html', {'dispatches': result, 'dispatch_filter': dispatch_query})

  else:
    dispatch_query = DispatchFilter()

  return render(request, 'drugapp/filter-dispatch-list.html', {'dispatch_filter': dispatch_query})